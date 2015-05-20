# coding=utf-8
__author__ = 'vladaoleynik'


from main import List
from bottle import route, run, request

redis = List.connection()


@route('/todo/tasks', method='GET')
def tasks_list():
    return List.print_all(redis, None)


@route('/todo/tasks/<name>', method='GET')
def get_task(name):
    return List.print_all(redis, name)


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


@route('/todo/tasks/<name>/<task_id:int>', method='PUT')
def edit_tasks(name, task_id):
    description = request.forms.get('description')
    deadline = request.forms.get('deadline')
    importance = request.forms.get('importance')
    if List.edit(redis, name, task_id, description, importance, deadline):
        return '500 Server error\n'
    else:
        return '200 OK\n'


@route('/todo/tasks', method='DELETE')
def clear_db():
    if List.delete(redis, None, 'all'):
        return '500 Server error\n'
    else:
        return '200 OK\n'


@route('/todo/tasks/<task_name>', method='DELETE')
def clear_db(task_name):
    if List.delete(redis, task_name, 'all'):
        return '500 Server error\n'
    else:
        return '200 OK\n'


run(host='localhost', port=8080, debug=True)
