class User: 
    
    def __init__(self, user_id, username=None, password=None, email=None, group = None):
        self.id = user_id
        self.username = username 
        self.password = password
        self.email = email
        self.in_group = group

    def add_to_group(self, group):
        self.in_group = group

class Group: 
    
    def __init__(self, group_id, name=None, projects = []):
        self.id = group_id
        self.name = name
        self.projects = projects

    def add_project(self, project):
        self.projects.append(project)

class Project: 

    def __init__(self, project_id, name=None, description=None, chart_link=None, tasks = []):
        self.id = project_id
        self.name = name
        self.tasks = tasks
        self.description = description
        self.chart_link = chart_link

    def add_task(self, task):
        self.tasks.append(task)

class Tasks:
    
    def __init__(self, task_id, title=None, description=None, start_date=None, end_date=None, assignees = []):
        self.id = task_id
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.assignees = assignees

    def add_assignee(self, assignee):
        self.assignees.append(assignee)