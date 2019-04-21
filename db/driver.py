from pyley import CayleyClient, GraphObject
from .models import *
import requests
import re


class DatabaseDriver():
    types = {
        "USER": User,
        "GROUP": Group,
        "PROJECT": Project,
        "TASK": Task
    }

    def __init__(self, address=""):

        self.client = CayleyClient()
        self.g = GraphObject()

    def get_user_by_id(self, user_id):
        query = self.g.V("user/" + str(user_id)).Out(["username", "password", "email", "in_group"], "pred").All()

        try:
            response = self.client.Send(query).result["result"]
            user = User(user_id)

            for i in response:
                setattr(user, i['pred'], i['id'])

            return user

        except:
            return None

    def _parse_object_response(self, response, label):
        created_objects = []
        objects = []
        for i in response:
            if not i['source_id'] in created_objects:
                objects.append(self.types[label](re.findall("\d+", i['source_id'])[0]))
                created_objects.append(i['source_id'])
            user = next((x for x in objects if x.id == re.findall("\d+", i['source_id'])[0]), None)
            if type(getattr(user, i['pred'])) == type(set()):
                getattr(user, i['pred']).add(i['id'])
            else:
                setattr(user, i['pred'], i['id'])

        return objects

    def _filter_by_label(self, label):

        query = "g.V().LabelContext(\"%s\").In().Tag(\"source_id\").LabelContext(null) \
            .Out([], \"pred\").All()" % (label)

        try:
            response = self.client.Send(query).result["result"]
            return self._parse_object_response(response, label)
        except:
            return None

    def _filter_by_parameter(self, parameter, value=None):
        if value is None:
            query = self.g.V().Out(parameter).All()
        else:
            query = self.g.V().Both(parameter).Is(*value).All()

        try:
            response = self.client.Send(query).result["result"]
            return set((i['id'] for i in response))
        except:
            return None

    def filter_by(self, node_type, value=None):

        upper_node_type = node_type.upper()

        if upper_node_type in self.types:
            result = self._filter_by_label(upper_node_type)

        else:
            result = self._filter_by_parameter(node_type, value)

        return result
