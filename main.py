# coding=utf-8
__author__ = 'vladaoleynik'

import redis
import json
import argparse


class List(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        self.tasks = dict()
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        if option_string == '-i':
            name = values
        if option_string == '-a':
            print self.name
            self.add(name, *values)
        if option_string == '-e':
            self.edit(name, *values)
        if option_string == '-d':
            self.delete(name, values)
        if option_string == '-p':
            self.print_all(name)

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
    parser = argparse.ArgumentParser(description='Work with Redis database.')
    parser.add_argument('args', metavar='N', nargs='?',
                        help='an integer for the accumulator')
    parser.add_argument('-i', '--init', action=List, nargs=1,
                        help='Initiating a new list')
    parser.add_argument('-a', '--add', action=List, nargs=4,
                        help='Adding task to list')
    parser.add_argument('-e', '--edit', action=List, nargs=4,
                        help='Editing task in list')
    parser.add_argument('-d', '--del', action=List,
                        help='Deleting task from list')
    parser.add_argument('-p', action=List, nargs=0,
                        help='Printing all the tasks in list')
    args = parser.parse_args()