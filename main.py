# coding=utf-8
__author__ = 'vladaoleynik'

import redis
import json


class Task(object):

    def __init__(self, task_id, description, priority, deadline):
        self.id = task_id
        self.context = dict(description=description, priority=priority, deadline=deadline)


class List(object):

    def __init__(self, name):
        self.tasks = dict()
        self.name = name
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def add(self, task_id, description, priority, deadline):
        tasks = self.r.get(self.name)
        if tasks is not None:
            tasks = self.decode_json(tasks)
        else:
            tasks = dict()
        task_id = str(task_id)
        tasks[task_id] = dict(description=description, priority=priority, deadline=deadline)
        self.push_to_redis(tasks)

    def delete(self, task_id):
        tasks = self.r.get(self.name)
        if tasks is not None:
            tasks = self.decode_json(tasks)
        else:
            raise "Database is empty. Nothing to delete."
        del tasks[str(task_id)]
        self.push_to_redis(tasks)

    def edit(self, task_id, description, priority, deadline):
        tasks = self.r.get(self.name)
        if tasks is not None:
            tasks = self.decode_json(tasks)
        else:
            raise "Database is empty. Nothing to edit"
        tasks[str(task_id)] = dict(description=description, priority=priority, deadline=deadline)
        self.push_to_redis(tasks)

    def print_all(self):
        tasks = self.r.get(self.name)
        if tasks is not None:
            tasks = self.decode_json(tasks)
        else:
            raise "Database is empty. Nothing to print"
        for key, value in tasks.iteritems():
            print("Task №%d: ") % (int(key))
            for k, v in value.iteritems():
                print("%s: %s") % (k, v)


    def push_to_redis(self, tasks):
        tasks_json = self.encode_json(tasks)
        self.r.set(self.name, tasks_json)

    def encode_json(self, task):
        return json.dumps(task, sort_keys=True, separators=(',', ': '))

    def decode_json(self, task):
        return json.loads(task)


if __name__ == '__main__':
    t = List('ToDo')
    t.add('5', 'b', 0, 15)
    t.add('3', 'c', 0, 15)
    t.edit('3', 'abc', 0, 15)
    t.add('1', 'abc', 0, 15)
    t.delete(1)
    t.print_all()