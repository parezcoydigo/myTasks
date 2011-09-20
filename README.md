# Overview

myTasks is a python program for interacting with Google Tasks through the command line. Tasks and can be displayed, added, marked as completed, cleared, or deleted. OAuth authentication is handled with some code based on Google's api examples.

# Requirements

myTasks uses optparse to manage command line args, and should work with Python 2.3.x or later. It requires the `google_api_python_client` [package](http://code.google.com/p/google-api-python-client/). As written, it also uses `keyring` to manage keys. For more information on initial authorization of the client, see this [post]() on my blog.

# Usage

For help or reminders on usage, use the `-h` option.  

List tasks: `myTasks.py -l`  
New task: `myTasks.py -n <ListName> <"Task"> <DueDate>`  
Update task: `myTasks.py -u <ListName> <TaskNumber>`  
Delete task: `myTasks.py -d <ListName> <TaskNumber>`   
Clear completed tasks: `myTasks.py -c`  

Listing tasks assigns a number to each task. It's this number that's needed to update or delete a task, so list them first.

For myself, I added an alias to my `.bash_profile` file pointing to the script named "tasks". So, listing tasks is `tasks -l`. 

