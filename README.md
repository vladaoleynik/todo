# REST API on Bottle framework
To work with API use curl, please!<br/>
<br/>
<strong> Add information</strong><br/>
Helps to add task to concrete task list.<br/>
/todo/tasks/<task_name> POST-method<br/>
Required data:<br/>
task description;<br/>
task importance;<br/>
task deadline;<br/>
Example: curl -X POST -d "description=0&deadline=0&importance=0" http://localhost:8080/todo/tasks
<br/>
<br/><strong>Edit information</strong><br/>
Helps to edit task in concrete task list.<br/>
/todo/tasks/<task_name>/<task_id:int> PUT-method<br/>
Required data (at least one of these items):<br/>
task description;<br/>
task importance;<br/>
task deadline;<br/>
Example: curl -X PUT -d "description=bla" http://localhost:8080/todo/tasks/list/1
<br/>
<br/><strong>Clearing the whole DB</strong><br/>
Deleting all the task lists.<br/>
/todo/tasks DELETE-method<br/>
Required data: none<br/>
Example: curl -X DELETE http://localhost:8080/todo/tasks
<br/>
<br/><strong>Clearing the task list</strong><br/>
Deleting all the tasks in task list.<br/>
/todo/tasks/<task_name> DELETE-method<br/>
Required data: none<br/>
Example: curl -X DELETE http://localhost:8080/todo/tasks/list
<br/>
<br/><strong>Deleting the task</strong><br/>
Deleting the task from task list.<br/>
/todo/tasks/<task_name>/<task_id> DELETE-method<br/>
Required data: none<br/>
Example: curl -X DELETE http://localhost:8080/todo/tasks/list/2
<br/>
<br/><strong>Printing all the task lists</strong><br/>
Printing the names of all task lists in our db.<br/>
/todo/tasks GET-method<br/>
Required data: none<br/>
Example: curl -X GET http://localhost:8080/todo/tasks
<br/>
<br/><strong>Printing all the tasks</strong><br/>
Printing all the tasks in task list.<br/>
/todo/tasks/<name> GET-method<br/>
Required data: none<br/>
Example: curl -X GET http://localhost:8080/todo/tasks/list

# Working with argparse

<strong>-i task_list_name -a args</strong> - adding task to the task_list_name list

<strong>-i task_list_name -e args</strong> - editing task in the task_list_name list

<strong>-i task_list_name -d all</strong> - deleting all the tasks from task_list_name list

<strong>-i task_list_name -d task_id</strong> - deleting all the task_id task from task_list_name list

<strong>-d all</strong> - deleting all the task lists in db

<strong>-p</strong> - printing names of all existing in db task lists

<strong>-i task_list_name -p</strong> - printing all the tasks from task_list_name list