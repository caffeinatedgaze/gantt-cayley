from requests.auth import HTTPBasicAuth
import plotly.figure_factory as ff
import plotly.tools as tools
import plotly.plotly as py
from random import randint
import requests

username = 'fenchelfen'
api_key = 'A813566osbTCR6NQ923L'

tools.set_credentials_file(username=username, api_key=api_key)

df = [
    dict(Task='Morning Sleep', Start='2016-01-01', Finish='2016-01-01 6:00:00', Resource='Sleep'),
    dict(Task='Breakfast', Start='2016-01-01 7:00:00', Finish='2016-01-01 7:30:00', Resource='Food'),
    dict(Task='Work', Start='2016-01-01 9:00:00', Finish='2016-01-01 11:25:00', Resource='Brain'),
    dict(Task='Break', Start='2016-01-01 11:30:00', Finish='2016-01-01 12:00:00', Resource='Rest'),
    dict(Task='Lunch', Start='2016-01-01 12:00:00', Finish='2016-01-01 13:00:00', Resource='Food'),
    dict(Task='Work', Start='2016-01-01 13:00:00', Finish='2016-01-01 17:00:00', Resource='Brain'),
    dict(Task='Exercise', Start='2016-01-01 17:30:00', Finish='2016-01-01 18:30:00', Resource='Cardio'),
    dict(Task='Post Workout Rest', Start='2016-01-01 18:30:00', Finish='2016-01-01 19:00:00', Resource='Rest'),
    dict(Task='Dinner', Start='2016-01-01 19:00:00', Finish='2016-01-01 20:00:00', Resource='Food'),
    dict(Task='Evening Sleep', Start='2016-01-01 21:00:00', Finish='2016-01-01 23:59:00', Resource='Sleep')
]


def create_chart(df, title):
    r = lambda: randint(0, 255)
    colors = ['#%02X%02X%02X' % (r(), r(), r()) for _ in range(len(df))]
    print(colors)
    fig = ff.create_gantt(df, colors=colors, title=title,
                          show_colorbar=True, bar_width=0.8, showgrid_x=True, showgrid_y=True)
    return py.plot(fig, filename='gantt-hours-minutes', world_readable=True)


def delete_chart(chart_link):
    index = int(chart_link.split('/').pop())
    table_name = username + ':' + str(index + 1)
    chart_name = username + ':' + str(index)
    _delete_plotly_obj(table_name)
    _delete_plotly_obj(chart_name)


def _delete_plotly_obj(fid):
    auth = HTTPBasicAuth(username, api_key)
    headers = {'Plotly-Client-Platform': 'python'}
    print(requests.post('https://api.plot.ly/v2/files/' + fid + '/trash',
                        auth=auth, headers=headers).status_code)
    print(requests.delete('https://api.plot.ly/v2/files/' + fid + '/permanent_delete',
                          auth=auth, headers=headers).status_code)
