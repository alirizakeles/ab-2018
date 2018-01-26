import falcon
import json

from graceful.serializers import BaseSerializer
from graceful.fields import StringField, BaseField
from graceful.resources.generic import RetrieveAPI, ListCreateAPI
from src.rest.rpc_client import RpcClient


api = application = falcon.API()


class ListOfStringsField(BaseField):
    """
    Represents the list of strings type field in our api.
    """
    def from_representation(self, data):
        return data

    def to_representation(self, value):
        return value


# this is how we represent cats in our API
class SubscriptionSerializer(BaseSerializer):
    # todo add validators to the fields.
    email = StringField("Email to send repository reports", allow_null=False)
    subscriptions = ListOfStringsField("List of subscribed github ids",
                                       allow_null=False)
    period = StringField("Notification period e.g. daily, or weekly",
                         allow_null=False)


class Subscription(RetrieveAPI, with_context=True):
    """
    """
    def __init__(self, rpc_client):
        self.rpc_client = rpc_client
        super(Subscription, self).__init__()
    serializer = SubscriptionSerializer()

    def retrieve(self, params, meta, **kwargs):
        pass


class SubscriptionList(ListCreateAPI, with_context=True):
    """
    """
    def __init__(self, rpc_client):
        self.rpc_client = rpc_client
        super(SubscriptionList, self).__init__()

    serializer = SubscriptionSerializer()

    def create(self, params, meta, **kwargs):
        validated = kwargs.get('validated')
        # todo make the rpc call and wait for response
        resp = self.rpc_client.rpc_call("subscribe", validated)
        print(resp)
        return resp


rpc_client = RpcClient()
api.add_route("/v1/subscriptions/{email}", Subscription(rpc_client))
api.add_route("/v1/subscriptions/", SubscriptionList(rpc_client))
