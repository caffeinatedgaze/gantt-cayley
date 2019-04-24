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

    def __init__(self, name, user_id):
        self.username = name
        self.id = user_id
        self.password = "12345"
        self.label = 'USER'
        self.email = self.gen_email()
        self.groups = []
        self.tasks = []

    def gen_email(self):
        domains = ['gantt.com', 'gmail.com', 'yandex.com']
        delimeter = '@'
        return self.username + delimeter + random.choice(domains)

    def add_group(self, group):
        self.groups.append(group)

    def add_task(self, task):
        self.tasks.append(task)


class Group:

    def __init__(self, group_id):
        self.id = group_id
        self.name = "Group" + str(self.id)
        self.label = "GROUP"
        self.projects = []
        self.users = []

    def add_project(self, project):
        self.projects.append(project)

    def add_user(self, user):
        self.users.append(user)


class Project:

    def __init__(self, project_id, description = "This is simple project"):
        self.id = project_id
        self.name = "Project" + str(self.id)
        self.label = "PROJECT"
        self.description = description
        self.tasks = []
        self.group = None

    def add_task(self, task):
        self.tasks.append(task)

class Task:

    task_descriptions = ['Fix bugs', 'Make login page', 'Payment system', 
                        'Buy bread', 'Test coverage at least 90%', 'Deploy', 
                        'Run server', 'Make it work', 'Relax', 'Just do it',
                        'Run', 'Clear configs', 'Walk my dog', 'Learn Django',
                        'Play with Cayley', 'Populate database', 'Play guitar',
                        'Hack society']

    def __init__(self, task_id):
        self.id = task_id
        self.start, self.end = get_random_times()
        self.label = "TASK"
        self.title = "Task" + str(task_id)
        self.description = random.choice(Task.task_descriptions)
        self.users = []
        self.project = None

    def add_user(self, user):
        self.users.append(user)


class Generator:

    filename = "generated_db.nq"
    prop_users = 0.5

    def __init__(self, people_per_group=5, groups_amount=500, projects_per_group=2, tasks_per_project=10):
        self.people_per_group = people_per_group
        self.groups_amount = groups_amount
        self.projects_per_group = projects_per_group
        self.tasks_per_project = tasks_per_project
        self.tasks_amount = groups_amount * projects_per_group * tasks_per_project
        self.projects_amount = projects_per_group * groups_amount
        with open('projecttitles', 'r') as f:
            self.project_descripts = json.load(f)
        with open('names', 'r') as f:
            self.usernames = json.load(f)
        
    def gen_task(self):
        task = Task(len(self.tasks))
        self.tasks.append(task)
        return task

    def gen_project(self):
        description = random.choice(["Let's do", 'New', 'Making', 'Updated', 'Build', 'Startup']) + ' ' + random.choice(self.project_descripts)
        project = Project(len(self.projects), description)
        self.projects.append(project)
        return project

    def gen_users(self):
        self.users_amount = int(len(self.usernames) * Generator.prop_users)
        for i in range(self.users_amount):
            name = self.usernames[i]
            user_id = i
            user = User(name, user_id)
            self.users.append(user)

    def gen_groups(self):
        for i in range(self.groups_amount):
            group = Group(i)
            self.groups.append(group)

    def link_data(self):
        for group in self.groups:
            people = random.randint(2, self.people_per_group)
            for j in range(people):
                person = random.choice(self.users)
                s = set()
                while person.id in s:
                    person = random.choice(self.users)
                s.add(person.id)
                group.add_user(person)
                person.add_group(group)
            for j in range(self.projects_per_group):
                project = self.gen_project()
                group.add_project(project)
                project.group = group

        for project in self.projects:
            delta = random.randint(0, 3)
            tasks_per_project = self.tasks_per_project + delta
            for j in range(tasks_per_project):
                task = self.gen_task()
                task.project = project
                project.add_task(task)

                people = random.randint(1, self.people_per_group)
                for i in range(people):
                    person = random.choice(project.group.users)
                    s = set()
                    while person.id in s:
                        person = random.choice(project.group.users)
                    s.add(person)
                    person.add_task(task)
                    task.add_user(person)

    def gen_data(self):
        self.users = []
        self.groups = []
        self.projects = []
        self.tasks = []

        self.gen_users()
        self.gen_groups()

        self.link_data()

        entities = len(self.users) + len(self.groups) + len(self.projects) + len(self.tasks)
        print('There are', entities, 'in .nq file')
        print(len(self.users), 'users')
        print(len(self.groups), 'groups')
        print(len(self.projects), 'projects')
        print(len(self.tasks), 'tasks')

    def dump_users(self, f):
        for user in self.users:
            line = "user/{} username {} {} .\n".format(user.id, user.username, user.label)
            f.write(line)
            line = "user/{} password {} .\n".format(user.id, user.password)
            f.write(line)
            line = "user/{} email {} .\n".format(user.id, user.email)
            f.write(line)
            for group in user.groups:
                line = "user/{} in_group group/{} .\n".format(user.id, group.id)
                f.write(line)

            f.write("\n")

        line = "{} last_id {} .\n\n".format(self.users[0].label, len(self.users) - 1)
        f.write(line)

    def dump_groups(self, f):
        for group in self.groups:
            line = "group/{} name {} {} .\n".format(group.id, group.name, group.label)
            f.write(line)
            for project in group.projects:
                line = "group/{} project project/{} .\n".format(group.id, project.id)
                f.write(line)

            f.write("\n")
                
        line = "{} last_id {} .\n\n".format(self.groups[0].label, len(self.groups) - 1)
        f.write(line)

    def dump_projects(self, f):
        for project in self.projects:
            line = "project/{} name {} {} .\n".format(project.id, project.name, project.label)
            f.write(line)
            line = "project/{} description \"{}\" .\n".format(project.id, project.description)
            f.write(line)
            for task in project.tasks:
                line = "project/{} task task/{} .\n".format(project.id, task.id)
                f.write(line)

            f.write("\n")

        line = "{} last_id {} .\n\n".format(self.projects[0].label, len(self.projects) - 1)
        f.write(line)

    def dump_tasks(self, f):
        for task in self.tasks:
            line = "task/{} title {} {} .\n".format(task.id, task.title, task.label)
            f.write(line)
            line = "task/{} description \"{}\" .\n".format(task.id, task.description)
            f.write(line)
            line = "task/{} start_date {} .\n".format(task.id, task.start)
            f.write(line)
            line = "task/{} end_date {} .\n".format(task.id, task.end)
            f.write(line)
            for user in task.users:
                line = "task/{} assignee user/{} .\n".format(task.id, user.id)
                f.write(line)

            f.write("\n")

        line = "{} last_id {} .\n\n".format(self.tasks[0].label, len(self.tasks) - 1)
        f.write(line)

    def dump(self):
        with open(Generator.filename, 'w') as f:
            self.dump_users(f)
            self.dump_groups(f)
            self.dump_projects(f)
            self.dump_tasks(f)

print("Doing ...\n")
gen = Generator()
gen.gen_data()
gen.dump()
print("\nDone!")