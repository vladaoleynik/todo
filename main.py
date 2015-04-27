# coding=utf-8
__author__ = 'vladaoleynik'

import redis
import json


class Task(object):

    def __init__(self, task_id, description, priority, deadline):
        self.id = task_id
        self.context = dict(description=description, priority=priority, deadline=deadline)


class List(Task):

    def __init__(self, name):
        self.tasks = dict()
        self.name = name
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def add(self, task_id, description, priority, deadline):
        tasks = self.pull_from_redis(False)
        task_id = str(task_id)
        tasks[task_id] = dict(description=description, priority=priority, deadline=deadline)
        self.push_to_redis(tasks)
        print("The task was successfully added")

    def delete(self, task_id='all'):
        if task_id == 'all':
            self.r.flushdb()
            print("Task list was successfully deleted")
        else:
            tasks = self.pull_from_redis()
            del tasks[str(task_id)]
            self.push_to_redis(tasks)
            print("The task was successfully deleted")

    def edit(self, task_id, description, priority, deadline):
        tasks = self.pull_from_redis()
        tasks[str(task_id)] = dict(description=description, priority=priority, deadline=deadline)
        self.push_to_redis(tasks)
        print("The task was successfully edited")

    def print_all(self):
        tasks = self.pull_from_redis(False)
        if tasks and tasks is not None:
            for key, value in tasks.iteritems():
                print("Task №%d: ") % (int(key))
                for k, v in value.iteritems():
                    print("%s: %s") % (k, v)
        else:
            print('Oops..smth went wrong. List is empty')

    def push_to_redis(self, tasks):
        tasks_json = self.encode_json(tasks)
        self.r.set(self.name, tasks_json)

    def pull_from_redis(self, flag=True):
        # flag - to decide whether we should raise an exception
        tasks = self.r.get(self.name)
        if tasks is not None and tasks:
            tasks = self.decode_json(tasks)
            return tasks
        else:
            if flag:
                raise IndexError("Oops..smth went wrong. Database is empty.")
            else:
                tasks = dict()
                return tasks

    def encode_json(self, task):
        return json.dumps(task, sort_keys=True, separators=(',', ': '))

    def decode_json(self, task):
        return json.loads(task)


if __name__ == '__main__':
    t = List('ToDo')
    t.delete()

