# coding=utf-8
__author__ = 'vladaoleynik'


from main import List
from bottle import route, run, request

redis = List.connection()


# print all the task lists
@route('/todo/tasks', method='GET')
def tasks_list():
    return List.print_all(redis, None)


# print all the tasks in concrete task list
@route('/todo/tasks/<name>', method='GET')
def get_task(name):
    return List.print_all(redis, name)


# add task to concrete task list
@route('/todo/tasks/<name>', method='POST')
def add_tasks(name):
    description = request.forms.get('description')
    deadline = request.forms.get('deadline')
    importance = request.forms.get('importance')
    if description != '' and deadline != '' and importance != '':
        if List.add(redis, name, description, importance, deadline):
            return '500 Server error\n'
        else:
            return '201 Create\n'


# edit task in concrete task list
@route('/todo/tasks/<name>/<task_id:int>', method='PUT')
def edit_tasks(name, task_id):
    description = request.forms.get('description')
    deadline = request.forms.get('deadline')
    importance = request.forms.get('importance')
    if List.edit(redis, name, task_id, description, importance, deadline):
        return '500 Server error\n'
    else:
        return '200 OK\n'


# delete all the task lists (the whole db)
@route('/todo/tasks', method='DELETE')
def clear_db():
    if List.delete(redis, None, 'all'):
        return '500 Server error\n'
    else:
        return '200 OK\n'


# delete the task list
@route('/todo/tasks/<task_name>', method='DELETE')
def clear_db(task_name):
    if List.delete(redis, task_name, 'all'):
        return '500 Server error\n'
    else:
        return '200 OK\n'


# delete the task from task list
@route('/todo/tasks/<task_name>/<task_id>', method='DELETE')
def clear_db(task_name, task_id):
    if List.delete(redis, task_name, task_id):
        return '500 Server error\n'
    else:
        return '200 OK\n'


run(host='localhost', port=8080, debug=True)
