# coding=utf-8
__author__ = 'vladaoleynik'


from main import List
from bottle import route, run, request

redis = List.connection()


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


@route('/todo/tasks', method='GET')
def tasks_list():
    if List.print_all(redis, None) is None:
        return 'Nothing to print'
    else:
        return List.print_all(redis, None)


@route('/todo/tasks/<name>')
def get_task(name):
    if List.print_all(redis, name) is None:
        return 'Nothing to print'
    else:
        return List.print_all(redis, name)
    return '404 Not Found'


run(host='localhost', port=8080, debug=True)
