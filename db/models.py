from gantt_cayley import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    from db import driver
    return driver.get_user_by_id(user_id)


class User(UserMixin):

    def __init__(self, user_id=None, username=None, password=None, email=None, group=None):
        self.id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.in_group = [] if group is None else group

    def add_to_group(self, group):
        self.in_group = group


class Group:

    def __init__(self, group_id=None, name=None, projects=None):
        self.id = group_id
        self.name = name
        self.project = [] if projects is None else projects

    def add_project(self, project):
        self.project.append(project)


class Project:

    def __init__(self, project_id=None, name=None, description=None, chart_link=None, tasks=None):
        self.id = project_id
        self.name = name
        self.description = description
        self.chart_link = chart_link
        self.task = [] if tasks is None else tasks

    def add_task(self, task):
        self.task.append(task)


class Task:

    def __init__(self, task_id=None, title=None, description=None, start_date=None, end_date=None, assignees=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.assignee = [] if assignees is None else assignees

    def add_assignee(self, assignee):
        self.assignee.append(assignee)
