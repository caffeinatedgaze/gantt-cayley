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
        type(User()): "USER",
        type(Group()): "GROUP",
        type(Project()): "PROJECT",
        type(Task()): "TASK"
    }

    def __init__(self, address=""):

        self.client = CayleyClient() if address == "" else CayleyClient(address)
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

    def _get_last_id_from_db(self, label):
        query = self.g.V(label).Out("last_id").All()
        response = self.client.Send(query).result['result']
        return int(response[0]['id']) if response != None else 0

    def _generate_new_id(self, label, type_):
        
        last_from_db = self._get_last_id_from_db(label)

        if last_from_db == 0:
            new_id = 1
        else: 
            new_id = last_from_db + 1
            self.client.DeleteQuad(label, "last_id", str(last_from_db))

        while True:
            query = self.g.V(type_+"/"+str(new_id)).All()
            response = self.client.Send(query).result['result']
            if response == None:
                break
            new_id += 1
         
        self.client.AddQuad(label, "last_id", str(new_id))

        return new_id

    # action should be "add" or "delete"
    def _generate_quads(self, object_, action, last_used_id = 0):
        attrs = object_.__dict__.items()

        quads = []

        object_id = last_used_id

        if type(object_) in self.labels:
            label = self.labels[type(object_)]
            type_ = label.lower()

            if action == "add":
                object_id = self._generate_new_id(label, type_)
            elif action == "delete":
                object_id = getattr(object_, "id")
            else: 
                return []

            str_id = type_+"/"+str(object_id)
        
            for key, value in attrs:
                if key != "id" and value != None and value != []:
                    quad = (str_id, key, value, label)
                    quads.append(quad)

        return quads

    def add_object(self, object_):
        self.add_objects(self, [object_])

    def add_objects(self, objects): 
        quads = []
        for obj in objects:
            quads += self._generate_quads(obj, "add")

        self.client.AddQuads(quads)

    def edit(self, old_object, new_object):
        old = self._generate_quads(old_object, "delete")
        new = self._generate_quads(new_object, "delete")

        self.client.DeleteQuads(old).result['result']
        self.client.AddQuads(new)

    def _update_last_used_id(self, quads):
        checked = []
        for q in quads:
            if not q[0] in checked:
                checked.append(q[0])
                type_ = re.findall(re.compile("[a-z]+"), q[0])[0]
                id_ = int(re.findall(re.compile("\d+"), q[0])[0])
                label = type_.upper()
                last_id = self._get_last_id_from_db(label)
                if id_ < last_id:
                    self.client.DeleteQuad(label, "last_id", str(last_id))
                    self.client.AddQuad(label, "last_id", str(id_))               
                                
    def delete_object(self, object_):
        self.delete_objects([object_])

    def delete_objects(self, objects):
        quads = []

        for obj in objects:
            quads += self._generate_quads(obj, "delete")
        
        self.client.DeleteQuads(quads)
        self._update_last_used_id(quads)
