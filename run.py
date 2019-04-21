from plotly.graph_objs.sankey import node

from gantt_cayley import app
from db import driver

print(driver.filter_by(node_type='USER'))
# for x in driver.filter_by(node_type='USER'):
#     print(x.username)

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0')
