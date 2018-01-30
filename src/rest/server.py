import falcon
import json
import redis
import pika
import os

from graceful.serializers import BaseSerializer
from graceful.fields import StringField, BaseField, IntField
from graceful.resources.generic import ListCreateAPI

RABBIT_HOST = os.getenv('RABBIT_HOST')
RABBIT_PORT = os.getenv('RABBIT_PORT', 5672)
VIRTUAL_HOST = os.getenv('VIRTUAL_HOST')
RABBIT_USER = os.getenv('RABBIT_USER')
RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)


api = application = falcon.API()
QUEUE_NAME = "scheduler_queue"

class JsonField(BaseField):
    """
    Represents the list of strings type field in our api.
    """
    def from_representation(self, data):
        return json.dumps(data)

    def to_representation(self, value):
        return json.loads(value)


class SubscriptionSerializer(BaseSerializer):
    #TODO: ADD VALIDATORS
    email = StringField("Email to send repository reports")
    subscriptions = JsonField("List of subscribed github ids")
    period = StringField("Notification period e.g. daily, or weekly")
    telegramID = StringField("Telegram ID")
    repoCount = IntField("Number of suggestions each time")


class SubscriptionList(ListCreateAPI, with_context=True):
    """
    """
    def __init__(self):
        super(SubscriptionList, self).__init__()
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBIT_HOST,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
            )
        )

        self.channel = connection.channel()

        self.channel.queue_declare(queue=QUEUE_NAME, durable=True)
    
        
    serializer = SubscriptionSerializer()

    def create(self, params, meta, **kwargs):
        validated = kwargs.get('validated')
        print(validated)
        value = json.dumps(validated)
        key = "temp:User:{}".format(validated["email"])
        self.redis_client.set(key, value)
        self.channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=value)
        return validated


api.add_route("/v1/subscriptions/", SubscriptionList())
