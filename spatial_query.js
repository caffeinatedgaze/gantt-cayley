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

  for (var i = 0; i < projects.length; i++) {
    temp = find_tasks(projects[i]['id'])
    tasks[projects[i]['id']] = []
  for (var j = 0; j < temp.length; j++) {
       tasks[projects[i]['id']].push(temp[j]['id'])
    }
    tasks[projects[i]['id']] = tasks[projects[i]['id']].length  
  }
  return tasks
}

function countTasksAndAssignees() {
  projects = get_projects()
  result = []
  for (var i = 0; i < projects.length; i++) {
    tasks = find_tasks(projects[i]['id'])
    result[i] = {}
    result[i]['project'] = projects[i]['id']
    result[i]['tasks'] = []
    result[i]['assignees'] = []
  for (var j = 0; j < tasks.length; j++) {
       result[i]['tasks'].push(tasks[j]['id'])
       
       people_for_tasks = find_assignees(tasks[j]['id'])
       for (var k = 0; k < people_for_tasks.length; k++) {
         result[i]['assignees'].push(people_for_tasks[k])
       }
    } 
    result[i]['assignees'] = result[i]['assignees'].filter( onlyUnique );
    result[i]['assignees'] = result[i]['assignees'].length
    result[i]['tasks'] = result[i]['tasks'].length
  }
  return result;
}

function cmp(a, b) {
  if (a['distance'] > b['distance'])
    return 1
  if (a['distance'] < b['distance'])
    return -1
  return 0
}

function spatialSearch(x, y, data) {
  for (var i = 0; i < data.length; i++) {
    data[i]['distance'] = Math.pow(data[i]['tasks'] - x, 2) + Math.pow(data[i]['assignees'] - y, 2)
    data[i]['distance'] = Math.sqrt(data[i]['distance'])
  }
  data.sort(cmp)
  data = data.splice(0, 5)
  for (var i = 0; i < data.length; i++) {
    data[i] = data[i]['project']
  }
  return data
}
var answer = spatialSearch(5, 2, countTasksAndAssignees())
g.Emit(answer)
