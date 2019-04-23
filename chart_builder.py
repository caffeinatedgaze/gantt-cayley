from requests.auth import HTTPBasicAuth
import plotly.figure_factory as ff
import plotly.tools as tools
import plotly.plotly as py
from random import randint, uniform
import requests

username = 'shittyinstagramvanhalen'
api_key = '4HaREPLKtBw2m0hLYDKh'

tools.set_credentials_file(username=username, api_key=api_key)


def create_chart(df, title):
    r = lambda: randint(0, 255)
    colors = ['#%02X%02X%02X' % (r(), r(), r()) for _ in range(len(df))]
    bar_width = uniform(0.4, 1) if len(df) < 5 else uniform(0.1, 0.3)
    fig = ff.create_gantt(df, colors=colors, title=title,
                          show_colorbar=True, bar_width=bar_width, showgrid_x=True, showgrid_y=True)
    return py.plot(fig, filename=title, world_readable=True, auto_open=False)


def define_data(tasks):
    df = []
    for task in tasks:
        df.append(
            dict(
                Task=task.title,
                Start=task.start_date,
                Finish=task.end_date
            )
        )
    return df


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
