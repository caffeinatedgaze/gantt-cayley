from chart_builder import delete_chart
from gantt_cayley import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    from db import driver
    return driver.get_user_by_id(user_id)


class User(UserMixin):

    def __init__(self, user_id=None, username=None, password=None, email=None, in_group=None):
        self.id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.in_group = [] if in_group is None else in_group

    def add_to_group(self, group):
        self.in_group = group


class Group:

    def __init__(self, group_id=None, name=None, project=None):
        self.id = group_id
        self.name = name
        if project is None:
            self.project = []
        else: 
            self.project = project if type(project) == type([]) else [project]

    def add_project(self, project):
        self.project.append(project)


class Project:

    def __init__(self, project_id=None, name=None, chart_link=None, description=None, task=None):
        self.id = project_id
        self.name = name
        self.description = description
        self.chart_link = chart_link
        if task is None:
            self.task = []
        else: 
            self.task = task if type(task) == type([]) else [task]

    def add_task(self, task):
        self.task.append(task)


class Task:

    def __init__(self, task_id=None, title=None, description=None, start_date=None, end_date=None, assignee=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        if assignee is None:
            self.assignee = []
        else: 
            self.assignee = assignee if type(assignee) == type([]) else [assignee]

    def add_assignee(self, assignee):
        self.assignee.append(assignee)
