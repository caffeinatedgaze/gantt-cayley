# Usage python param1:int param2:int

from requests import post
from json import dumps, loads
from sys import argv, stderr

api_url = u'http://localhost:64210/api/v1/query/gizmo?limit=-1'

if len(argv) < 3:
    print('Got params?', flush=stderr)

try:
    param1 = int(argv[1])
    param2 = int(argv[2])
    print(param1, param2)
except ValueError:
    print('Non-int params', flush=stderr)
    raise ValueError

spatial_query = open('spatial_query.js').read()
spatial_query = spatial_query.replace('{@param1}', str(param1))
spatial_query = spatial_query.replace('{@param2}', str(param2))
# spatial_query += "\n g.Emit(forPlot)"
spatial_query += "\n g.Emit(top)"


# query = 'g.V().Out(\'username\').All()'

r = post(api_url, data=spatial_query)

print(r.status_code, r.reason)

result = loads(r.text).get('result', None)
if result is None:
    print(loads(r.text))
else:
    result = result[0]

print(dumps(result, indent=4))
