import pika
import threading
from time import sleep
import json
import uuid
import time
from pika.exceptions import ConnectionClosed
from falcon import HTTPBadRequest, HTTPForbidden


RPC_ERROR = {
    -32006: HTTPBadRequest,
    -32007: HTTPForbidden,
}


class UnKnownException(Exception):
    def __init__(self, *args, **kwargs):
        super(UnKnownException, self).__init__()


class RpcClient(object):
    internal_lock = threading.Lock()

    def __init__(self,
                 exchange="ab18-.exchange",
                 connection_params=None,
                 rabbitmq_user="ab18",
                 rabbitmq_pass="1",
                 ):

        self.connection_params = connection_params if connection_params else {
            "host": "localhost",
            "port": 5672,
            "virtual_host": "ab18",
        }

        self.credentials = pika.PlainCredentials(rabbitmq_user,
                                                 rabbitmq_pass)

        self.exchange = exchange
        self.exchange_declared = False
        self.connection = None
        self.channel = None
        self.callback_queue = None

        self.open_connection()
        thread = threading.Thread(target=self._process_data_events)
        thread.setDaemon(True)
        thread.start()

    def _process_data_events(self):
        """
        In order to come over the "ERROR:pika.adapters.base_connection:Socket Error on fd 34: 104"
        adapted from:
            https://github.com/pika/pika/issues/439
            https://github.com/pika/pika/issues/439#issuecomment-36452519
            https://github.com/eandersson/python-rabbitmq-examples/blob/master/Flask-examples/pika_async_rpc_example.py
        """
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

        while True:
            with self.internal_lock:
                self.connection.process_data_events()
            sleep(0.05)

    def open_connection(self):
        """
        Connect to RabbitMQ.
        """

        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    **self.connection_params,
                    credentials=self.credentials
                )
            )

        if not self.channel or self.channel.is_closed:
            self.channel = self.connection.channel()

        if not self.exchange_declared:
            self.channel.exchange_declare(
                exchange=self.exchange,
                exchange_type='topic',
                durable=True,
                auto_delete=False
            )
            self.exchange_declared = True

        result = self.channel.queue_declare(queue='ab18-.kurs-kuyruk', exclusive=True)
        self.callback_queue = result.method.queue

    def close_connection(self):
        """
        Close active connection.
        """

        if self.channel:
            self.channel.close()

        if self.connection:
            self.connection.close()

        self.connection, self.channel = None, None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def rpc_call(self, method, params, blocking=True, time_limit=10):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.message_properties = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self.corr_id
        }

        try:
            if not self.connection or self.connection.is_closed or not self.channel or self.channel.is_closed:
                with self.internal_lock:
                    self.open_connection()

            with self.internal_lock:
                self.channel.basic_publish(
                    exchange=self.exchange,
                    routing_key='rpc_queue',
                    properties=pika.BasicProperties(
                        reply_to=self.callback_queue,
                        correlation_id=self.corr_id),
                    body=json.dumps(self.message_properties, ensure_ascii=False))

        except ConnectionClosed:
            with self.internal_lock:
                self.close_connection()
                self.open_connection()
            return self.rpc_call(method, params, blocking=blocking,
                                 time_limit=time_limit)
        except Exception as e:
            self.response = {"error": {"code": -32603,
                                       "message": "Can not connect AMQP or another error occured!"}, }
            self.close_connection()

        if not blocking and self.response is None:
            return params  # "Job is queued"

        deadline = time.time() + time_limit

        while self.response is None:
            time_limit = deadline - time.time()
            if time_limit <= 0:
                self.response = {
                    "error": {"code": -32003, "message": "Worker timeout"}, }

        if "result" in self.response:
            return self.response['result']

        if "error" in self.response:
            error, msg = RPC_ERROR.get(self.response['error']['code'],
                                       UnKnownException), self.response['error']['message']
            raise error(description=msg)


