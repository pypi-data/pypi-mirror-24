#    Copyright 2014 Rackspace
#    Copyright 2016 Blue Box, an IBM Company
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from oslo_config import cfg
from oslo_db import exception as odb_exceptions
from oslo_utils import excutils
import pecan
from wsme import types as wtypes
from wsmeext import pecan as wsme_pecan

from octavia.api.v2.controllers import base
from octavia.api.v2.controllers import l7policy
from octavia.api.v2.types import listener as listener_types
from octavia.common import constants
from octavia.common import data_models
from octavia.common import exceptions
from octavia.common import stats
from octavia.db import api as db_api
from octavia.db import prepare as db_prepare


CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class ListenersController(base.BaseController):
    RBAC_TYPE = constants.RBAC_LISTENER

    def __init__(self):
        super(ListenersController, self).__init__()
        self.handler = self.handler.listener

    def _get_db_listener(self, session, id):
        """Gets a listener object from the database."""
        listener = super(ListenersController, self)._get_db_listener(
            session, id)
        load_balancer_id = listener.load_balancer_id
        db_listener = self.repositories.listener.get(
            session, load_balancer_id=load_balancer_id, id=id)
        if not db_listener:
            LOG.info("Listener %s not found.", id)
            raise exceptions.NotFound(
                resource=data_models.Listener._name(), id=id)
        return db_listener

    @wsme_pecan.wsexpose(listener_types.ListenerRootResponse, wtypes.text)
    def get_one(self, id):
        """Gets a single listener's details."""
        context = pecan.request.context.get('octavia_context')
        db_listener = self._get_db_listener(context.session, id)

        self._auth_validate_action(context, db_listener.project_id,
                                   constants.RBAC_GET_ONE)

        result = self._convert_db_to_type(db_listener,
                                          listener_types.ListenerResponse)
        return listener_types.ListenerRootResponse(listener=result)

    @wsme_pecan.wsexpose(listener_types.ListenersRootResponse, wtypes.text,
                         [wtypes.text], ignore_extra_args=True)
    def get_all(self, project_id=None, fields=None):
        """Lists all listeners."""
        pcontext = pecan.request.context
        context = pcontext.get('octavia_context')

        query_filter = self._auth_get_all(context, project_id)

        db_listeners, links = self.repositories.listener.get_all(
            context.session, show_deleted=False,
            pagination_helper=pcontext.get(constants.PAGINATION_HELPER),
            **query_filter)
        result = self._convert_db_to_type(
            db_listeners, [listener_types.ListenerResponse])
        if fields is not None:
            result = self._filter_fields(result, fields)
        return listener_types.ListenersRootResponse(
            listeners=result, listeners_links=links)

    def _test_lb_and_listener_statuses(
            self, session, lb_id, id=None,
            listener_status=constants.PENDING_UPDATE):
        """Verify load balancer is in a mutable state."""
        lb_repo = self.repositories.load_balancer
        if id:
            if not self.repositories.test_and_set_lb_and_listeners_prov_status(
                    session, lb_id, constants.PENDING_UPDATE,
                    listener_status, listener_ids=[id]):
                LOG.info("Load Balancer %s is immutable.", lb_id)
                db_lb = lb_repo.get(session, id=lb_id)
                raise exceptions.ImmutableObject(resource=db_lb._name(),
                                                 id=lb_id)
        else:
            if not lb_repo.test_and_set_provisioning_status(
                    session, lb_id, constants.PENDING_UPDATE):
                db_lb = lb_repo.get(session, id=lb_id)
                LOG.info("Load Balancer %s is immutable.", db_lb.id)
                raise exceptions.ImmutableObject(resource=db_lb._name(),
                                                 id=lb_id)

    def _validate_pool(self, session, lb_id, pool_id):
        """Validate pool given exists on same load balancer as listener."""
        db_pool = self.repositories.pool.get(
            session, load_balancer_id=lb_id, id=pool_id)
        if not db_pool:
            raise exceptions.NotFound(
                resource=data_models.Pool._name(), id=pool_id)

    def _reset_lb_status(self, session, lb_id):
        # Setting LB back to active because this should be a recoverable error
        self.repositories.load_balancer.update(
            session, lb_id,
            provisioning_status=constants.ACTIVE)

    def _validate_create_listener(self, lock_session, lb_id, listener_dict):
        """Validate listener for wrong protocol or duplicate listeners

        Update the load balancer db when provisioning status changes.
        """
        if (listener_dict and
            listener_dict.get('insert_headers') and
            list(set(listener_dict['insert_headers'].keys()) -
                 set(constants.SUPPORTED_HTTP_HEADERS))):
            raise exceptions.InvalidOption(
                value=listener_dict.get('insert_headers'),
                option='insert_headers')

        try:
            sni_containers = listener_dict.pop('sni_containers', [])
            db_listener = self.repositories.listener.create(
                lock_session, **listener_dict)
            if sni_containers:
                for container in sni_containers:
                    sni_dict = {'listener_id': db_listener.id,
                                'tls_container_id': container.get(
                                    'tls_container_id')}
                    self.repositories.sni.create(lock_session, **sni_dict)
                db_listener = self.repositories.listener.get(
                    lock_session, id=db_listener.id)
            return db_listener
        except odb_exceptions.DBDuplicateEntry as de:
            column_list = ['load_balancer_id', 'protocol_port']
            constraint_list = ['uq_listener_load_balancer_id_protocol_port']
            if ['id'] == de.columns:
                raise exceptions.IDAlreadyExists()
            elif (set(column_list) == set(de.columns) or
                  set(constraint_list) == set(de.columns)):
                raise exceptions.DuplicateListenerEntry(
                    port=listener_dict.get('protocol_port'))
        except odb_exceptions.DBError:
            raise exceptions.InvalidOption(value=listener_dict.get('protocol'),
                                           option='protocol')

    def _send_listener_to_handler(self, session, db_listener):
        try:
            LOG.info("Sending Creation of Listener %s to handler",
                     db_listener.id)
            self.handler.create(db_listener)
        except Exception:
            with excutils.save_and_reraise_exception(
                    reraise=False), db_api.get_lock_session() as lock_session:
                self._reset_lb_status(
                    lock_session, lb_id=db_listener.load_balancer_id)
                # Listener now goes to ERROR
                self.repositories.listener.update(
                    lock_session, db_listener.id,
                    provisioning_status=constants.ERROR)
        db_listener = self._get_db_listener(session, db_listener.id)
        result = self._convert_db_to_type(db_listener,
                                          listener_types.ListenerResponse)
        return listener_types.ListenerRootResponse(listener=result)

    @wsme_pecan.wsexpose(listener_types.ListenerRootResponse,
                         body=listener_types.ListenerRootPOST, status_code=201)
    def post(self, listener_):
        """Creates a listener on a load balancer."""
        listener = listener_.listener
        context = pecan.request.context.get('octavia_context')

        load_balancer_id = listener.loadbalancer_id
        listener.project_id = self._get_lb_project_id(
            context.session, load_balancer_id)

        self._auth_validate_action(context, listener.project_id,
                                   constants.RBAC_POST)

        if (not CONF.api_settings.allow_tls_terminated_listeners and
                listener.protocol == constants.PROTOCOL_TERMINATED_HTTPS):
            raise exceptions.DisabledOption(
                value=constants.PROTOCOL_TERMINATED_HTTPS, option='protocol')

        lock_session = db_api.get_session(autocommit=False)
        if self.repositories.check_quota_met(
                context.session,
                lock_session,
                data_models.Listener,
                listener.project_id):
            lock_session.rollback()
            raise exceptions.QuotaException

        listener_dict = db_prepare.create_listener(
            listener.to_dict(render_unsets=True), None)

        if listener_dict['default_pool_id']:
            self._validate_pool(context.session, load_balancer_id,
                                listener_dict['default_pool_id'])

        try:
            self._test_lb_and_listener_statuses(
                lock_session, lb_id=load_balancer_id)

            db_listener = self._validate_create_listener(
                lock_session, load_balancer_id, listener_dict)
            lock_session.commit()
        except Exception:
            with excutils.save_and_reraise_exception():
                lock_session.rollback()

        return self._send_listener_to_handler(context.session, db_listener)

    def _graph_create(self, lock_session, listener_dict,
                      l7policies=None, pool_name_ids=None):
        load_balancer_id = listener_dict['load_balancer_id']
        listener_dict = db_prepare.create_listener(
            listener_dict, load_balancer_id)
        l7policies = listener_dict.pop('l7policies', l7policies)
        if listener_dict.get('default_pool_id'):
            self._validate_pool(lock_session, load_balancer_id,
                                listener_dict['default_pool_id'])
        db_listener = self._validate_create_listener(
            lock_session, load_balancer_id, listener_dict)

        # Now create l7policies
        new_l7ps = []
        for l7p in l7policies:
            l7p['project_id'] = db_listener.project_id
            l7p['load_balancer_id'] = load_balancer_id
            l7p['listener_id'] = db_listener.id
            redirect_pool = l7p.pop('redirect_pool', None)
            if redirect_pool:
                pool_name = redirect_pool['name']
                pool_id = pool_name_ids.get(pool_name)
                if not pool_id:
                    raise exceptions.SingleCreateDetailsMissing(
                        type='Pool', name=pool_name)
                l7p['redirect_pool_id'] = pool_id
            new_l7ps.append(l7policy.L7PolicyController()._graph_create(
                lock_session, l7p))
        return db_listener, new_l7ps

    @wsme_pecan.wsexpose(listener_types.ListenerRootResponse, wtypes.text,
                         body=listener_types.ListenerRootPUT, status_code=200)
    def put(self, id, listener_):
        """Updates a listener on a load balancer."""
        listener = listener_.listener
        context = pecan.request.context.get('octavia_context')
        db_listener = self._get_db_listener(context.session, id)
        load_balancer_id = db_listener.load_balancer_id

        self._auth_validate_action(context, db_listener.project_id,
                                   constants.RBAC_PUT)

        # TODO(rm_work): Do we need something like this? What do we do on an
        # empty body for a PUT?
        if not listener:
            raise exceptions.ValidationException(
                detail='No listener object supplied.')

        if listener.default_pool_id:
            self._validate_pool(context.session, load_balancer_id,
                                listener.default_pool_id)
        self._test_lb_and_listener_statuses(context.session, load_balancer_id,
                                            id=id)

        try:
            LOG.info("Sending Update of Listener %s to handler", id)
            self.handler.update(db_listener, listener)
        except Exception:
            with excutils.save_and_reraise_exception(
                    reraise=False), db_api.get_lock_session() as lock_session:
                self._reset_lb_status(
                    lock_session, lb_id=db_listener.load_balancer_id)
                # Listener now goes to ERROR
                self.repositories.listener.update(
                    lock_session, db_listener.id,
                    provisioning_status=constants.ERROR)
        db_listener = self._get_db_listener(context.session, id)
        result = self._convert_db_to_type(db_listener,
                                          listener_types.ListenerResponse)
        return listener_types.ListenerRootResponse(listener=result)

    @wsme_pecan.wsexpose(None, wtypes.text, status_code=204)
    def delete(self, id):
        """Deletes a listener from a load balancer."""
        context = pecan.request.context.get('octavia_context')
        db_listener = self._get_db_listener(context.session, id)
        load_balancer_id = db_listener.load_balancer_id

        self._auth_validate_action(context, db_listener.project_id,
                                   constants.RBAC_DELETE)

        self._test_lb_and_listener_statuses(
            context.session, load_balancer_id,
            id=id, listener_status=constants.PENDING_DELETE)

        try:
            LOG.info("Sending Deletion of Listener %s to handler",
                     db_listener.id)
            self.handler.delete(db_listener)
        except Exception:
            with excutils.save_and_reraise_exception(
                    reraise=False), db_api.get_lock_session() as lock_session:
                self._reset_lb_status(
                    lock_session, lb_id=db_listener.load_balancer_id)
                # Listener now goes to ERROR
                self.repositories.listener.update(
                    lock_session, db_listener.id,
                    provisioning_status=constants.ERROR)

    @pecan.expose()
    def _lookup(self, id, *remainder):
        """Overridden pecan _lookup method for custom routing.

        Currently it checks if this was a stats request and routes
        the request to the StatsController.
        """
        if id and len(remainder) and remainder[0] == 'stats':
            return StatisticsController(listener_id=id), remainder[1:]


class StatisticsController(base.BaseController, stats.StatsMixin):
    RBAC_TYPE = constants.RBAC_LISTENER

    def __init__(self, listener_id):
        super(StatisticsController, self).__init__()
        self.id = listener_id

    @wsme_pecan.wsexpose(listener_types.StatisticsRootResponse, wtypes.text,
                         status_code=200)
    def get(self):
        context = pecan.request.context.get('octavia_context')
        db_listener = self._get_db_listener(context.session, self.id)
        if not db_listener:
            LOG.info("Listener %s not found.", id)
            raise exceptions.NotFound(
                resource=data_models.Listener._name(),
                id=id)

        self._auth_validate_action(context, db_listener.project_id,
                                   constants.RBAC_GET_STATS)

        listener_stats = self.get_listener_stats(context.session, self.id)

        result = self._convert_db_to_type(
            listener_stats, listener_types.ListenerStatisticsResponse)
        return listener_types.StatisticsRootResponse(stats=result)
