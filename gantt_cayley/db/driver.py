from pyley import CayleyClient, GraphObject
import requests
from models import *

class DatabaseDriver():

    def __init__(self, address=""):

        self.client = CayleyClient()
        self.g = GraphObject()

    def get_user_by_id(self, id):
        # query = self.g.V("user:"+str(id)).Out().All()
        query = self.g.V("user:"+str(id)).Out(["username", "password", "email"], "pred").All()
        response = self.client.Send(query)
        return response.result["result"]

    def _parse_user(self, response):

        created_user = []
        users = []
        for i in response:
            if not i['user_id'] in created_user:
                users.append(User(i['user_id']))
                created_user.append(i['user_id'])
            user = next((x for x in users if x.id == i['user_id']), None)
            setattr(user, i['pred'], i['id'])

        return users

    def _filter_by_label(self, label, value=None):

        if label == "USER": 
            query = "g.V().LabelContext(\"%s\").In().Tag(\"user_id\").LabelContext(null) \
                .Out([\"username\", \"password\", \"email\", \"in_group\"], \"pred\").All()" % (label)        
            response = self.client.Send(query).result["result"] 

            return self._parse_user(response)

        if label == "GROUP":
            query = self.g.V().Out(["name", "project"], "pred").All()

        if label == "PROJECT":
            query = self.g.V().Out("name", "pred").All()

        # query = "g.V().LabelContext(\"%s\").In().LabelContext(null).Out().All()" % (label)
        response = self.client.Send(query).result["result"] 
        # return set((i['id'] for i in response))
        return response

    def _filter_by_parameter(self, parameter, value=None):
        if value is None:
            query = self.g.V().Out(parameter).All()
        else:
            query = self.g.V().Both(parameter).Is(*value).All()

        response = self.client.Send(query).result["result"]
        return set((i['id'] for i in response))
    

    def filter_by(self, node_type, value=None):

        query = "g.V().Labels().All()"
        labels = self.client.Send(query).result["result"]
        upper_node_type = node_type.upper()

        if {'id': upper_node_type} in labels:
            result = self._filter_by_label(upper_node_type, value)
            
        else:
            result = self._filter_by_parameter(node_type, value)
        
        return None or result


