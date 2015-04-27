# coding=utf-8
__author__ = 'vladaoleynik'

import redis
import json


class Task(object):
    def __init__(self, task_id, description, priority, deadline):
        self.id = task_id
        self.context = dict(description=description, priority=priority, deadline=deadline)


class List(Task):

    def __init__(self, *args):
        self.tasks = dict()
        for arg in args:
            self.tasks[arg.id] = arg.context

    def add(self, task_id, description, priority, deadline):
        task_id = str(task_id)
        self.tasks[task_id] = dict(description=description, priority=priority, deadline=deadline)

    def delete(self, task_id):
        task_id = str(task_id)
        del self.tasks[task_id]

    def get_json(self):
        return json.dumps(self.tasks, sort_keys=True, indent=4, separators=(',', ': '))

    def init_redis(self):
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        r = redis.Redis(connection_pool=pool)



if __name__ == '__main__':
    t = List(Task('1', 'a', 0, 15))
    print t.get_json()