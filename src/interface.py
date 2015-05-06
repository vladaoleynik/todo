# coding=utf-8
__author__ = 'user'

from Tkinter import *
from ttk import *
import logging
import redis
import json


class List(object):
    # log configuration
    # all the errors are to be found in mylog.log
    logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG, filename='mylog.log')
    tasks = dict()
    # connecting to Redis
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    # dumb manipulations with tasks list name

    # json encode
    @staticmethod
    def encode_json(task):
        return json.dumps(task, sort_keys=True, separators=(',', ': '))

    @staticmethod
    # json decode
    def decode_json(task):
        return json.loads(task)

    @staticmethod
    # json encode
    def get_args(entry):
        args = entry.get()
        return args.split(',')

    @staticmethod
    def add_window():

        def add_task():
            args = List.get_args(a_entry)
            name = args[0]
            task_id = args[1]
            description = args[2]
            priority = args[3]
            deadline = args[4]
            tasks = List.pull_from_redis(name, False)
            task_id = str(task_id)
            tasks[task_id] = dict(description=description, priority=priority, deadline=deadline)
            List.push_to_redis(name, tasks)
            label = Label(a_window, text="The task was successfully added")
            label.pack()
            logging.info('The task was successfully added')

        a_window = Toplevel()
        a_window.title('Добавить в Redis')
        a_window.geometry('500x400+300+200')  # ширина=500, высота=400, x=300, y=200
        a_label = Label(a_window, text="Print arguments divided by comas")
        a_label.pack()
        a_entry = Entry(a_window, width=400)
        a_entry.pack()
        a_button = Button(a_window, bg="red", text="Добавить", command=add_task)
        a_button.pack()

    @staticmethod
    def delete_window():

        def delete_db():
            List.r.flushdb()
            d_label = Label(d_window, text="All the database was successfully cleared")
            d_label.pack()
            logging.info("All the database was successfully cleared")

        def delete_task_list():
            invite_label = Label(d_window, text="Print task name to delete")
            invite_label.pack()
            d_entry = Entry(d_window, width=400)
            d_entry.pack()

            def delete():
                args = List.get_args(d_entry)
                name = args[0]
                List.r.delete(name)
                d_label = Label(d_window, text="Task list was successfully deleted")
                d_label.pack()
                logging.info("Task list was successfully deleted")

            delete_button = Button(d_window, bg="red", text="Удалить", command=delete)
            delete_button.pack()

        def delete_task():
            invite_label = Label(d_window, text="Print task name and task id to delete")
            invite_label.pack()
            d_entry = Entry(d_window, width=400)
            d_entry.pack()

            def delete():
                args = List.get_args(d_entry)
                name = args[0]
                task_id = args[1]
                tasks = List.pull_from_redis(name)
                del tasks[str(task_id)]
                List.push_to_redis(name, tasks)
                d_label = Label(d_window, text="The task was successfully deleted")
                d_label.pack()
                logging.info("Task list was successfully deleted")

            delete_button = Button(d_window, bg="red", text="Удалить", command=delete)
            delete_button.pack()

        d_window = Toplevel()
        d_window.title('Удалить из Redis')
        d_window.geometry('500x400+300+200')  # ширина=500, высота=400, x=300, y=200
        d_db_button = Button(d_window, bg="red", text="Clear DB", command=delete_db)
        d_db_button.pack()
        d_task_list_button = Button(d_window, bg="red", text="Clear task list", command=delete_task_list)
        d_task_list_button.pack()
        d_button = Button(d_window, bg="red", text="Delete Task", command=delete_task)
        d_button.pack()

    @staticmethod
    def edit_window():

        def edit_task():
            args = List.get_args(e_entry)
            name = args[0]
            task_id = args[1]
            description = args[2]
            priority = args[3]
            deadline = args[4]
            tasks = List.pull_from_redis(name)
            tasks[str(task_id)] = dict(description=description, priority=priority, deadline=deadline)
            List.push_to_redis(name, tasks)
            label = Label(e_window, text="The task was successfully edited")
            label.pack()
            logging.info("The task was successfully edited")

        e_window = Toplevel()
        e_window.title('Редактировать задание в Redis')
        e_window.geometry('500x400+300+200')  # ширина=500, высота=400, x=300, y=200
        e_label = Label(e_window, text="Print arguments divided by comas")
        e_label.pack()
        e_entry = Entry(e_window, width=400)
        e_entry.pack()
        e_button = Button(e_window, bg="red", text="Изменить", command=edit_task)
        e_button.pack()

    @staticmethod
    def print_window():

        def print_all():
            # print("Here are the names of all the task lists:")
            tasks = List.r.keys()
            if tasks:
                # print("Here are the names of all the task lists:")
                label = Label(p_window, text="Here are the names of all the task lists:")
                label.pack()
                for task in tasks:
                    label1 = Label(p_window, text=task)
                    label1.pack()
            else:
                label1 = Label(p_window, text='Oops..smth went wrong. DB is empty')
                label1.pack()
                logging.warning('Oops..smth went wrong. DB is empty')

        def print_task_list():
            invite_label = Label(p_window, text="Enter task list name to print")
            invite_label.pack()
            p_entry = Entry(p_window, width=400)
            p_entry.pack()

            def printt():
                # printing all the tasks in the task list
                args = List.get_args(p_entry)
                name = args[0]
                tasks = List.pull_from_redis(name, False)
                if tasks and tasks is not None:
                    for key, value in tasks.iteritems():
                        string = "Task №" + str(key)
                        label1 = Label(p_window, text=string)
                        label1.pack()
                        for k, v in value.iteritems():
                            string = k + ': ' + v
                            label1 = Label(p_window, text=string)
                            label1.pack()
                else:
                    label1 = Label(root, text='Oops..smth went wrong. List is empty')
                    label1.pack()
                    logging.warning('Oops..smth went wrong. List is empty')

            p_button = Button(p_window, bg="red", text="Вывести", command=printt)
            p_button.pack()

        p_window = Toplevel()
        p_window.title('Вывести из Redis')
        p_window.geometry('500x400+300+200')  # ширина=500, высота=400, x=300, y=200
        p_task_list_button = Button(p_window, bg="red", text="Print all task lists in DB", command=print_all)
        p_task_list_button.pack()
        p_button = Button(p_window, bg="red", text="Print concrete task list", command=print_task_list)
        p_button.pack()

    @staticmethod
    # pushing in db
    def push_to_redis(name, tasks):
        tasks_json = List.encode_json(tasks)
        List.r.set(name, tasks_json)

    # pulling from db
    @staticmethod
    def pull_from_redis(name, flag=True):
        # flag - to decide whether we should raise an exception
        tasks = List.r.get(name)
        if tasks is not None and tasks:
            tasks = List.decode_json(tasks)
            return tasks
        else:
            if flag:
                logging.error("Oops..smth went wrong. Database is empty.")
            else:
                tasks = dict()
                return tasks


root = Tk()
style = Style()
style.theme_use('clam')
root.title('Менеджер задач для Redis')
root.geometry('500x400+300+200')  # ширина=500, высота=400, x=300, y=200
label = Label(root, text="Что вы хотите сделать?")
label.pack()
add_button = Button(root, text="Добавить", command=List.add_window)
add_button.pack()
delete_button = Button(root, text="Удалить", command=List.delete_window)
delete_button.pack()
edit_button = Button(root, text="Изменить", command=List.edit_window)
edit_button.pack()
print_button = Button(root, text="Вывести", command=List.print_window)
print_button.pack()
root.mainloop()