# coding=utf-8
__author__ = 'vladaoleynik'

import redis
import json
import argparse
import logging


class List(argparse.Action):

    logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG, filename='mylog.log')

    def __call__(self, parser, namespace, values, option_string):
        self.tasks = dict()
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        setattr(namespace, self.dest, values)
        name = None
        if namespace.init is not None:
            name = str(namespace.init[0])
        if option_string == '-a':
            self.add(name, *values)
        if option_string == '-e':
            self.edit(name, *values)
        if option_string == '-d':
            self.delete(name, values)
        if option_string == '-p':
            self.print_all(name)

    def add(self, name, task_id, description, priority, deadline):
        tasks = self.pull_from_redis(name, False)
        task_id = str(task_id)
        tasks[task_id] = dict(description=description, priority=priority, deadline=deadline)
        self.push_to_redis(name, tasks)
        logging.info('The task was successfully added')

    def delete(self, name, task_id):
        if task_id == 'all' and name is None:
            self.r.flushdb()
            logging.info("All the database was successfully cleared")
        elif name and task_id == 'all':
            self.r.delete(name)
            logging.info("Task list was successfully deleted")
        else:
            tasks = self.pull_from_redis(name)
            del tasks[str(task_id)]
            self.push_to_redis(name, tasks)
            logging.info("The task was successfully deleted")

    def edit(self, name, task_id, description, priority, deadline):
        tasks = self.pull_from_redis(name)
        tasks[str(task_id)] = dict(description=description, priority=priority, deadline=deadline)
        self.push_to_redis(name, tasks)
        logging.info("The task was successfully edited")

    def print_all(self, name):
        if name is None:
            tasks = self.r.keys()
            if tasks:
                print("Here are the names of all the task lists:")
                for task in tasks:
                    print task
            else:
                logging.warning('Oops..smth went wrong. List is empty')
        else:
            tasks = self.pull_from_redis(name, False)
            if tasks and tasks is not None:
                for key, value in tasks.iteritems():
                    print("Task №%d: ") % (int(key))
                    for k, v in value.iteritems():
                        print("%s: %s") % (k, v)
            else:
                logging.warning('Oops..smth went wrong. List is empty')

    def push_to_redis(self, name, tasks):
        tasks_json = self.encode_json(tasks)
        self.r.set(name, tasks_json)

    def pull_from_redis(self, name, flag=True):
        # flag - to decide whether we should raise an exception
        tasks = self.r.get(name)
        if tasks is not None and tasks:
            tasks = self.decode_json(tasks)
            return tasks
        else:
            if flag:
                logging.error("Oops..smth went wrong. Database is empty.")
            else:
                tasks = dict()
                return tasks

    def encode_json(self, task):
        return json.dumps(task, sort_keys=True, separators=(',', ': '))

    def decode_json(self, task):
        return json.loads(task)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Work with Redis database.')
    parser.add_argument('-i', '--init', action=List, nargs=1,
                        help='Initiating a new list')
    parser.add_argument('-a', action=List, nargs=4,
                        help='Adding task to list')
    parser.add_argument('-e', action=List, nargs=4,
                        help='Editing task in list')
    parser.add_argument('-d', action=List,
                        help='Deleting task from list')
    parser.add_argument('-p', action=List, nargs=0,
                        help='Printing all the tasks in list')
    args = parser.parse_args()