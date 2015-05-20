# coding=utf-8
__author__ = 'vladaoleynik'

import redis
import json
import argparse
import logging


class List(argparse.Action):
    """
    Main class to do all the manipulations with Redis
    """
    # log configuration
    # all the errors and stuff are to be found in mylog.log
    logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG, filename='mylog.log')

    def __call__(self, parser, namespace, values, option_string):
        """
        main method when dealing with console
        :param parser:
        :param namespace:
        :param values:
        :param option_string:
        """
        self.tasks = dict()
        # connecting to Redis
        self.r = List.connection()
        # dumb manipulations with tasks list name
        setattr(namespace, self.dest, values)
        name = None
        # choosing a method depending on args
        if namespace.init is not None:
            name = str(namespace.init[0])
        if option_string == '-a':
            List.add(self.r, name, *values)
        if option_string == '-e':
            List.edit(self.r, name, *values)
        if option_string == '-d':
            List.delete(self.r, name, values)
        if option_string == '-p':
            print List.print_all(self.r, name)

    @staticmethod
    def connection():
        """
        function to connect to the DB
        :return: connection with Redis
        """
        return redis.StrictRedis(host='localhost', port=6379, db=0)

    @staticmethod
    def add(redis, name, description, priority, deadline):
        """
        Function to add tasks to our task list in Redis
        :param redis: Redis connection
        :param name: task name
        :param description: task description
        :param priority: task priority
        :param deadline: deadline for task
        """
        tasks = List.pull_from_redis(redis, name, False)
        task_id = str(len(tasks)+1)
        tasks[task_id] = dict(description=description, priority=priority, deadline=deadline)
        List.push_to_redis(redis, name, tasks)
        logging.info('The task was successfully added')
        return 0

    @staticmethod
    def delete(redis, name, task_id):
        """
        Function to delete entries (tasks or whole task lists) from Redis
        :param redis: Redis connection
        :param name: task name
        :param task_id: task id
        """
        if task_id == 'all' and name is None:
            # db clear
            redis.flushdb()
            logging.info("All the database was successfully cleared")
            return 0
        elif name and task_id == 'all':
            # deleting a single task list
            redis.delete(name)
            logging.info("Task list was successfully deleted")
            return 0
        else:
            # deleting a single task from concrete list
            tasks = List.pull_from_redis(redis, name)
            del tasks[str(task_id)]
            List.push_to_redis(redis, name, tasks)
            logging.info("The task was successfully deleted")
            return 0

    @staticmethod
    def edit(redis, name, task_id, description='', priority='', deadline=''):
        """
        Function to edit entries in our task lists
        :param redis: Redis connection
        :param name: task name
        :param task_id: task id
        :param description: task description
        :param priority: task priority
        :param deadline: deadline for task
        """
        tasks = List.pull_from_redis(redis, name)
        desc = tasks[str(task_id)]["description"]
        pr = tasks[str(task_id)]["priority"]
        dl = tasks[str(task_id)]["deadline"]
        if description:
            desc = description
        if priority:
            pr = priority
        if deadline:
            dl = deadline
        tasks[str(task_id)] = dict(description=desc, priority=pr, deadline=dl)
        List.push_to_redis(redis, name, tasks)
        logging.info("The task was successfully edited")
        return 0

    @staticmethod
    def print_all(redis, name):
        """
        Function to print all the entries in our database
        :param redis: Redis connection
        :param name: task name
        """
        if name is None:
            # printing names of all the task lists in db
            tasks = redis.keys()
            if tasks:
                stri = "Here are the names of all the task lists:\n"
                for task in tasks:
                    stri += task + '\n'
                return stri
            else:
                logging.warning('Oops..smth went wrong. List is empty')
                return 'Nothing to print.'
        else:
            # printing all the tasks in the task list
            stri = ''
            tasks = List.pull_from_redis(redis, name, False)
            if tasks and tasks is not None:
                for key, value in tasks.iteritems():
                    stri += 'Task ' + key + ': ' + '\n'
                    for k, v in value.iteritems():
                        stri += k + ': ' + v + '\n'
                    stri += '--------------\n'
                return stri
            else:
                logging.warning('Oops..smth went wrong. List is empty')
                return 'Nothing to print.'

    # pushing in db
    @staticmethod
    def push_to_redis(redis, name, tasks):
        """
        Helper function to push data to Redis
        :param redis: Redis connection
        :param name: task name
        :param tasks: data to push
        """
        tasks_json = List.encode_json(tasks)
        redis.set(name, tasks_json)

    # pulling from db
    @staticmethod
    def pull_from_redis(redis, name, flag=True):
        """
        Helper function to pull data from Redis
        :param redis: Redis connection
        :param name: task name
        :param flag:
        :return: pulled data
        """
        # flag - to decide whether we should raise an exception
        tasks = redis.get(name)
        if tasks is not None and tasks:
            tasks = List.decode_json(tasks)
            return tasks
        else:
            if flag:
                logging.error("Oops..smth went wrong. Database is empty.")
            else:
                tasks = dict()
                return tasks

    # json encode
    @staticmethod
    def encode_json(task):
        """
        Helper function to encode data in JSON
        :param task: data to encode
        :return: encoded data
        """
        return json.dumps(task, sort_keys=True, separators=(',', ': '))

    # json decode
    @staticmethod
    def decode_json(task):
        """
        Helper function to decode data from JSON
        :param task: data to decode
        :return: decoded data
        """
        return json.loads(task)


if __name__ == '__main__':
    # more info about how to use all this stuff - in README.md
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