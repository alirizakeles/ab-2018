import falcon
import json
import redis
import pika

from graceful.serializers import BaseSerializer
from graceful.fields import StringField, BaseField, IntField
from graceful.resources.generic import RetrieveAPI, ListCreateAPI

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
        self.redis_client = redis.Redis()
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='10.21.251.26', 
            virtual_host='ab18-vhost',
            credentials=pika.PlainCredentials('ab18-user', 'microservices')))
    
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
