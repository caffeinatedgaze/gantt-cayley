import random
import json
from datetime import datetime
from datetime import timedelta


def get_random_times():
    year = 2019
    month = random.choice([i for i in range(1, 13)])
    day = random.choice([i for i in range(1, 28)])

    start = str(year) + '-' + str(month) + '-' + str(day)
    start = datetime.strptime(start, '%Y-%m-%d')

    month = 30
    delta = random.choice([month, 2 * month, 3 * month, 6 * month])
    end = start + timedelta(days=delta)

    return datetime.strftime(start, '%Y-%m-%d'), datetime.strftime(end, '%Y-%m-%d')


class User:

    def __init__(self, name, user_id, group_id):
        self.username = name
        self.id = user_id
        self.group_id = group_id
        self.password = "12345"
        self.label = 'USER'
        self.gen_email()

    def gen_email(self):
        domains = ['gantt.com', 'gmail.com']
        delimeter = '@'
        self.email = self.username + delimeter + random.choice(domains)


class Group:

    def __init__(self, group_id):
        self.id = group_id
        self.name = "Group" + str(self.id)
        self.label = "GROUP"
        self.projects = []

    def add_project(self, project):
        self.projects.append(project)


class Project:

    def __init__(self, project_id):
        self.id = project_id
        self.name = "Project" + str(self.id)
        self.label = "PROJECT"
        self.description = "This is simple project"
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

class Task:

    def __init__(self, task_id):
        self.id = task_id
        self.start, self.end = get_random_times()
        self.label = "TASK"
        self.title = "Task" + str(task_id)
        self.description = "This is simple task"
        self.assignee = []

    def add_assignee(self, user_id):
        self.assignee.append(user_id)


class Generator:

    filename = "generated_db.nq"
    prop_users = 0.5

    def __init__(self, group_amount=3, projects_per_group=2, tasks_per_project=10):
        self.group_amount = group_amount
        self.projects_per_group = projects_per_group
        self.tasks_per_project = tasks_per_project
        
    def gen_tasks(self, group_id, project):
        for i in range(self.tasks_per_project):
            task = Task(len(self.tasks))
            people = random.randint(1, self.group_amount)
            first = group_id * self.group_amount
            last = first + people
            for i in range(first, last):
                task.add_assignee(i)
            self.tasks.append(task)
            project.add_task(task)

    def gen_data(self):
        with open('names', 'r') as f:
            usernames = json.load(f)
        self.users = []
        self.groups = []
        self.projects = []
        self.tasks = []
        for i in range(int(len(usernames) * Generator.prop_users)):
            group_id = i // self.group_amount
            name = usernames[i]
            user_id = i
            user = User(name, user_id, group_id)
            self.users.append(user)

            if i % self.group_amount == 0:
                group = Group(group_id)

                for i in range(self.projects_per_group):
                    project = Project(len(self.projects))
                    self.gen_tasks(group.id, project)
                    group.add_project(project)
                    self.projects.append(project)

                self.groups.append(group)

        entities = len(self.users) + len(self.groups) + len(self.projects) + len(self.tasks)
        print('There are', entities, 'in .nq file')

    def dump_users(self, f):
        for user in self.users:
            line = "user/{} username {} {} .\n".format(user.id, user.username, user.label)
            f.write(line)
            line = "user/{} password {} {} .\n".format(user.id, user.password, user.label)
            f.write(line)
            line = "user/{} email {} {} .\n".format(user.id, user.email, user.label)
            f.write(line)
            line = "user/{} in_group group/{} {} .\n".format(user.id, user.group_id, user.label)
            f.write(line)

            f.write("\n")

    def dump_groups(self, f):
        for group in self.groups:
            line = "group/{} name {} {} .\n".format(group.id, group.name, group.label)
            f.write(line)
            for project in group.projects:
                line = "group/{} project project/{} {} .\n".format(group.id, project.id, group.label)
                f.write(line)

            f.write("\n")

    def dump_projects(self, f):
        for project in self.projects:
            line = "project/{} name {} {} .\n".format(project.id, project.name, project.label)
            f.write(line)
            line = "project/{} description \"{}\" {} .\n".format(project.id, project.description, project.label)
            f.write(line)
            for task in project.tasks:
                line = "project/{} task task/{} {} .\n".format(project.id, task.id, project.label)
                f.write(line)

            f.write("\n")

    def dump_tasks(self, f):
        for task in self.tasks:
            line = "task/{} title {} {} .\n".format(task.id, task.title, task.label)
            f.write(line)
            line = "task/{} description \"{}\" {} .\n".format(task.id, task.description, task.label)
            f.write(line)
            line = "task/{} start_date {} {} .\n".format(task.id, task.start, task.label)
            f.write(line)
            line = "task/{} end_date {} {} .\n".format(task.id, task.end, task.label)
            f.write(line)
            for user_id in task.assignee:
                line = "task/{} assignee user/{} {} .\n".format(task.id, user_id, task.label)
                f.write(line)

            f.write("\n")

    def dump(self):
        with open(Generator.filename, 'w') as f:
            self.dump_users(f)
            self.dump_groups(f)
            self.dump_projects(f)
            self.dump_tasks(f)


gen = Generator()
gen.gen_data()
gen.dump()
