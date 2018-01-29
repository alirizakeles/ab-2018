import falcon
import json
import redis

from graceful.serializers import BaseSerializer
from graceful.fields import StringField, BaseField, IntField
from graceful.resources.generic import RetrieveAPI, ListCreateAPI
#from src.rest.rpc_client import RpcClient


api = application = falcon.API()


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
        #self.rpc_client = rpc_client
        super(SubscriptionList, self).__init__()
        self.redisClient = redis.Redis()

    serializer = SubscriptionSerializer()

    def create(self, params, meta, **kwargs):
        validated = kwargs.get('validated')
        print(validated)
        value = json.dumps(validated)
        key = "temp:User:" + validated["email"]
        self.redisClient.set(key, value)
        return validated
        # todo make the rpc call and wait for response
        #resp = self.rpc_client.rpc_call("subscribe", validated)
        #print(resp)
        #return resp


#rpc_client = RpcClient()
api.add_route("/v1/subscriptions/", SubscriptionList())
