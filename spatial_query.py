from requests import post
from json import dumps, loads

api_url = u'http://localhost:64210/api/v1/query/gizmo?limit=-1'

spatial_query = open('spatial_query.js').read()
# query = 'g.V().Out(\'username\').All()'

r = post(api_url, data=spatial_query)

print(r.status_code)

result = loads(r.text).get('result', None)
print(len(result))
print(dumps(result, indent=4))
