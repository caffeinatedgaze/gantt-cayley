from pyley import CayleyClient, GraphObject
from .models import User, Group, Task, Project
import requests
import re

class DatabaseDriver():
    types = {
        "USER": User,
        "GROUP": Group,
        "PROJECT": Project,
        "TASK": Task
    }

    labels = {
        type(User): "USER",
        type(Group): "GROUP",
        type(Project): "PROJECT",
        type(Task): "TASK"
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

    def _update_attr(self, obj, dict):
        if type(getattr(obj, dict['pred'])) == type([]):
            if not re.findall("\d+", dict['id'])[0] in getattr(obj, dict['pred']):
                getattr(obj, dict['pred']).append(re.findall("\d+", dict['id'])[0])
        else:
            setattr(obj, dict['pred'], dict['id'])

    def get_object_by_id(self, object_type, object_id):

        obj_id = object_type + "/" + object_id
        return self._get_object_by_id(obj_id)

    # object_id in form "type/id"
    def _get_object_by_id(self, object_id):
        pattern = re.findall(re.compile("[a-z]+"), object_id)
        if len(pattern) != 1:
            return None
        label = pattern[0].upper()
        
        if label in self.types:
            query = self.g.V(object_id).Out(tags="pred").All()

            try:
                response = self.client.Send(query).result["result"]
                
                new_object = self.types[label](re.findall("\d+", object_id)[0])
                
                for i in response:
                    self._update_attr(new_object, i)
            except: 
                return None

            return new_object

        return None

    def _parse_object_response(self, response, label):
        created_objects = []
        objects = []
        for i in response:
            if not i['source_id'] in created_objects:
                objects.append(self.types[label](re.findall("\d+", i['source_id'])[0]))
                created_objects.append(i['source_id'])
            next_object = next((x for x in objects if x.id == re.findall("\d+", i['source_id'])[0]), None)
            self._update_attr(next_object, i)

        return objects

    def _filter_by_label(self, label):

        query = "g.V().LabelContext(\"%s\").In().Tag(\"source_id\").LabelContext(null) \
            .Out([], \"pred\").All()" % (label)

        try:
            response = self.client.Send(query).result["result"]
            return self._parse_object_response(response, label)
        except:
            return []

    def _filter_by_parameter(self, parameter, value=None):
        if value is None:
            query = self.g.V().Out(parameter).All()
        else:
            query = self.g.V().Both(parameter).Is(*value).All()

        try:
            response = self.client.Send(query).result["result"]
            return list(set((i['id'] for i in response)))
        except:
            return []

    def filter_by(self, node_type, value=None):

        upper_node_type = node_type.upper()

        if upper_node_type in self.types:
            result = self._filter_by_label(upper_node_type)

        else:
            result = self._filter_by_parameter(node_type, value)

        return result

    def get_users(self, relation, value):
        result = self._filter_by_label('USER')
        return [x for x in result if getattr(x, relation) == value]
