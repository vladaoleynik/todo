__author__ = 'vladaoleynik'

import unittest
from src import main


class Test(unittest.TestCase):

    def test_connection(self):
        """
        Testing connection to Redis
        """
        r = main.List.connection()
        self.assertTrue(r.ping(), "Connection failed.")

    def test_add(self):
        """
        Testing adding entries to Redis
        """
        r = main.List.connection()
        main.List.add(r, "ToDo", 1, "Buy apples", 2, "20.05.2015")
        task = r.get("ToDo")
        self.assertTrue(task, "No such entry in DB. Adding failed.")

    def test_edit(self):
        """
        Testing editing entries in Redis
        """
        r = main.List.connection()
        main.List.add(r, "ToDo", 1, "Buy apples", 2, "20.05.2015")
        main.List.edit(r, "ToDo", 1, "Buy bananas, not apples", 2, "20.05.2015")
        task = main.List.pull_from_redis(r, "ToDo", False)
        if task and task is not None:
            check = task["1"]["description"] == "Buy bananas, not apples"
        self.assertTrue(check, "Editing failed.")

    def test_delete_task(self):
        """
        Testing deleting a single task from task list
        """
        check = False
        r = main.List.connection()
        main.List.add(r, "ToDo", 1, "Buy apples", 2, "20.05.2015")
        main.List.delete(r, "ToDo", 1)
        task = main.List.pull_from_redis(r, "ToDo", False)
        for key in task.iterkeys():
            if key == "1":
                check = True
        self.assertFalse(check, "Deleting task failed.")

    def test_delete_list(self):
        """
        Testing deleting a whole task list
        """
        r = main.List.connection()
        main.List.add(r, "ToDo", 1, "Buy apples", 2, "20.05.2015")
        main.List.delete(r, "ToDo", "all")
        task = r.get("ToDo")
        self.assertFalse(task, "Deleting task list failed.")


if __name__ == "main":
    unittest.main()
