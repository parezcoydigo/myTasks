# Overview

myTasks is a python script for interacting with Google Tasks through the command line. Tasks can be displayed, added, marked as completed, cleared, or deleted. OAuth authentication is handled with some code based on Google's api examples.

# Requirements

<<<<<<< HEAD
myTasks uses optparse to manage command line args, and should work with Python 2.3.x or later. It requires the `google_api_python_client` [package](http://code.google.com/p/google-api-python-client/). As written, it also uses `keyring` to manage keys. For more information on initial authorization of the client, see this [post]() on my blog.
=======
## Dependencies ##

* myTasks uses `argparse` to manage command line args. For Python versions prior to 2.7, the [`argparse` module](http://pypi.python.org/pypi/argparse) must be installed with either pip or easy_install: `pip install argparse` or `easy_install argparse`.  

* myTasks requires the `google_api_python_client` [package](http://code.google.com/p/google-api-python-client/). Follow in download and installation instructions there.  

* myTasks as written also uses `keyring` to manage keys. [`keyring`](http://pypi.python.org/pypi/keyring) supports a number of OS keychain services, including OSX's Keychain. To install, use`pip` or `easy_install`: `pip install keyring`.  myTasks uses `keyring` to store the client_secret provided by Google's [API Console](https://code.google.com/apis/console/). To store a key, from the python interpreter in the terminal, enter:   
`>>> import keyring`  
`>>> keyring.set_password('application name', 'username', 'password')`
where password = your client_secret.  
 
## Authorization ##

As with other applications that require authentication to interact with google services, your Tasks app needs to be authorized to make requests. So, for initial set-up there are two things you must do.  

1. Register your new application with google’s [API Console](https://code.google.com/apis/console/) by activating the Google Task API, and providing the requested information for a new app. This process will give you a ClientID, a ClientSecret Key, and an Application Developer Key that are necessary to authenticate the application.

2. Download and install the google API python developer’s library. I first installed using easy_install, but it didn’t work. So, you should use download the tar package, unzip it, open the terminal, change directory to the unzipped folder, and execute the command sudo python setup.py install.

3. Authenticate the application the first time you run the script from the command line. There will be a dialogue to approve access to your Tasks data. Paste the link provided into your browser, accept the access to your Tasks, then paste the provided key back into the terminal when asked for it.  


>>>>>>> Rewritten for v0.3.

# Usage

For help or reminders on usage, use the `-h` option.  

usage: tasks [option] arg1 arg2 arg3

optional arguments:  
  -h, --help            show this help message and exit  

  -l [optional ListName]  
                        Lists tasks. For a single list, pass the list name.  

  -n [ListName "Task" YYYY-MM-DD]
                        Adds new task. Pass the name of the task list and the new task as arguments in double quotes. For example:  tasks -n Main "Add this task to the Main list."

  -c                    
						Clears completed tasks from your lists. Takes no arguments.  

  -u [ListName TaskNumber]  
                        Updates a designated task as completed. Pass the name of the list and the number of the task. The number is available by first listing tasks with the -l command. For example: tasks -u Main 1. This command would mark the first message on the Main list as completed.  

  -d [ListName TaskNumber]    
                        Deletes a designated task. Pass the name of the list
                        and the number of the task. The number is available by first listing tasks with the -l command. For example: tasks -d Main 1. This command would delete the first message from the Main list.   

  -R [old ListName new ListName]    
                        Renames a task list. Pass the old list name and the
                        new list name. For example: tasks -R Main Home. This
                        command would rename the Main list as the Home list.  

  -D [target listName]   
						Delete a task list. Pass the targeted list name. For example: tasks -D Main. This command would delete the Main task list.  


For myself, I added an alias to my `.bash_profile` file pointing to the script named "tasks". So, listing tasks is `tasks -l`. 

