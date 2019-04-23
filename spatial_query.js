function get_projects() {
  to_proj = graph.Vertex().Tag('proj_name').LabelContext('PROJECT').In().LabelContext(null)
  return g.V().Follow(to_proj).TagArray()
}

function find_tasks(proj_name) {
  tasks = g.V(proj_name).Out('task').TagArray()
  return tasks
}

function find_assignees(task_name) {
  assignees = g.V(task_name).Out('assignee').TagArray()
  new_arr = []
  for (var i = 0; i < assignees.length; i++) {
    temp = assignees[i]['id']

    new_arr.push(temp)
  }

  return new_arr
}

function onlyUnique(value, index, self) {
    return self.indexOf(value) === index;
}

function countTasks() {
  var projects = get_projects()
  var tasks = {}

  for (var i = 0; i < 100; i++) {
    temp = find_tasks(projects[i]['id'])
    tasks[projects[i]['id']] = []
	for (var j = 0; j < temp.length; j++){
       tasks[projects[i]['id']].push(temp[j]['id'])
    }
  }
  g.Emit(tasks)
}

function countAssignees() {
  projects = get_projects()
  people = {}
  for (var i = 0; i < 100; i++) {
    tasks = find_tasks(projects[i]['id'])
    people[projects[i]['id']] = []
    for (var j = 0; j < tasks.length; j++) {
      people_for_tasks = find_assignees(tasks[j]['id'])
      for (var k = 0; k < people_for_tasks.length; k++) {
        people[projects[i]['id']].push(people_for_tasks[k])
      }
    }
    people[projects[i]['id']] = people[projects[i]['id']].filter( onlyUnique );
    people[projects[i]['id']] = people[projects[i]['id']].length
  }
  return people;
}

countTasks()


g.Emit('It\'s alive!')