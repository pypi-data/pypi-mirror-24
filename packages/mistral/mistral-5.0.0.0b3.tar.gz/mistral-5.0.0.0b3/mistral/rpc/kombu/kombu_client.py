# Copyright 2015 - Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from six import moves

import kombu
from oslo_log import log as logging

from mistral import config as cfg
from mistral import exceptions as exc
from mistral.rpc import base as rpc_base
from mistral.rpc.kombu import base as kombu_base
from mistral.rpc.kombu import kombu_hosts
from mistral.rpc.kombu import kombu_listener
from mistral import utils


LOG = logging.getLogger(__name__)

CONF = cfg.CONF

CONF.import_opt('rpc_response_timeout', 'mistral.config')


class KombuRPCClient(rpc_base.RPCClient, kombu_base.Base):
    def __init__(self, conf):
        super(KombuRPCClient, self).__init__(conf)

        kombu_base.set_transport_options()

        self._register_mistral_serialization()

        self.topic = conf.topic
        self.server_id = conf.host

        self._hosts = kombu_hosts.KombuHosts(CONF)

        self.exchange = CONF.control_exchange
        self.virtual_host = CONF.oslo_messaging_rabbit.rabbit_virtual_host
        self.durable_queue = CONF.oslo_messaging_rabbit.amqp_durable_queues
        self.auto_delete = CONF.oslo_messaging_rabbit.amqp_auto_delete
        self._timeout = CONF.rpc_response_timeout
        self.routing_key = self.topic

        hosts = self._hosts.get_hosts()

        self._connections = []

        for host in hosts:
            conn = self._make_connection(
                host.hostname,
                host.port,
                host.username,
                host.password,
                self.virtual_host
            )
            self._connections.append(conn)

        self.conn = self._connections[0]

        # Create exchange.
        exchange = self._make_exchange(
            self.exchange,
            durable=self.durable_queue,
            auto_delete=self.auto_delete
        )

        # Create queue.
        self.queue_name = utils.generate_unicode_uuid()
        self.callback_queue = kombu.Queue(
            self.queue_name,
            exchange=exchange,
            routing_key=self.queue_name,
            durable=False,
            exclusive=True,
            auto_delete=True
        )

        self._listener = kombu_listener.KombuRPCListener(
            connections=self._connections,
            callback_queue=self.callback_queue
        )

        self._listener.start()

    def _wait_for_result(self, correlation_id):
        """Waits for the result from the server.

        Waits for the result from the server, checks every second if
        a timeout occurred. If a timeout occurred - the `RpcTimeout` exception
        will be raised.
        """
        try:
            return self._listener.get_result(correlation_id, self._timeout)
        except moves.queue.Empty:
            raise exc.MistralException("RPC Request timeout")

    def _call(self, ctx, method, target, async_=False, **kwargs):
        """Performs a remote call for the given method.

        :param ctx: authentication context associated with mistral
        :param method: name of the method that should be executed
        :param kwargs: keyword parameters for the remote-method
        :param target: Server name
        :param async: bool value means whether the request is
            asynchronous or not.
        :return: result of the method or None if async.
        """
        correlation_id = utils.generate_unicode_uuid()

        body = {
            'rpc_ctx': ctx.convert_to_dict(),
            'rpc_method': method,
            'arguments': self._serialize_message(kwargs),
            'async': async_
        }

        LOG.debug("Publish request: {0}".format(body))

        try:
            if not async_:
                self._listener.add_listener(correlation_id)

            # Publish request.
            with kombu.producers[self.conn].acquire(block=True) as producer:
                producer.publish(
                    body=body,
                    exchange=self.exchange,
                    routing_key=self.topic,
                    reply_to=self.queue_name,
                    correlation_id=correlation_id,
                    delivery_mode=2
                )

            # Start waiting for response.
            if async_:
                return

            result = self._wait_for_result(correlation_id)
            res_type = result[kombu_base.TYPE]
            res_object = result[kombu_base.RESULT]

            if res_type == 'error':
                raise res_object
            else:
                res_object = self._deserialize_message(res_object)['body']

        finally:
            if not async_:
                self._listener.remove_listener(correlation_id)

        return res_object

    def sync_call(self, ctx, method, target=None, **kwargs):
        return self._call(ctx, method, async_=False, target=target, **kwargs)

    def async_call(self, ctx, method, target=None, **kwargs):
        return self._call(ctx, method, async_=True, target=target, **kwargs)
