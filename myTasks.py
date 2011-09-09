#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
myTasks
v0.2

Created by Chad Black, 09-07-2011.
"""

from optparse import OptionParser

import gflags
import httplib2
import keyring
import sys


from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run


def listTasks():
	tasklists = service.tasklists().list().execute()
	for tasklist in tasklists['items']:
		print tasklist['title']
		listID=tasklist['id']
		tasks = service.tasks().list(tasklist=listID).execute()
		n=1
		for task in tasks['items']:
			dueDate=''
			if task['title'] == None: pass
			else:
				if 'due' in task: 
					fullDueDate=str(task['due'])
					dueDate=fullDueDate[:10] 
					task['taskNum'] = n
					print '    '+str(n)+'. '+task['title']+' : '+dueDate
					n += 1
		print

def newTask(opts):
	listName = opts[0]
	task = {
	 	'title': opts[1], 
	 	'due': opts[2]+'T12:00:00.000Z',
		}					
	tasklists = service.tasklists().list().execute()
	listID = None
	for tasklist in tasklists['items']:
		if listName == tasklist['title']:
			listID=tasklist['id']
			break
	if listID == None:
		tasklist = {
	  	'title': listName,
	  	}
		result = service.tasklists().insert(body=tasklist).execute()
		listID = result['id']				
	newTask = service.tasks().insert(tasklist=listID, body=task).execute()
	print 'Completed.'

def clearTask():
	tasklists = service.tasklists().list().execute()
	for tasklist in tasklists['items']:
		listID = tasklist['id']
		service.tasks().clear(tasklist=listID, body='').execute()
	print 'Cleared.'

def delTask(opts):
	listName= opts[0]
	taskNumber = int(opts[1])

# match list off of list name		
	tasklists=service.tasklists().list().execute()
	for tasklist in tasklists['items']:
		if listName == tasklist['title']:
			listID=tasklist['id']
			break
			
# select and delete task
	tasks = service.tasks().list(tasklist=listID).execute()
	newList = tasks['items']
	selectTask = newList[taskNumber-1]
	taskID = selectTask['id']
	service.tasks().delete(tasklist=listID, task=taskID).execute()
	print "Completed."

def updateTask(opts):
	listName = opts[0]
	taskNumber = int(opts[1])		
	tasklists=service.tasklists().list().execute()
	for tasklist in tasklists['items']:
		if listName == tasklist['title']:
			listID=tasklist['id']
			break
	tasks = service.tasks().list(tasklist=listID).execute()
	newList = tasks['items']
	selectTask = newList[taskNumber-1]
	taskID = selectTask['id']
	
	chooseTask = service.tasks().get(tasklist=listID, task=taskID).execute()
	chooseTask['status'] = 'completed'
	markIt = service.tasks().update(tasklist=listID, task=chooseTask['id'], body=chooseTask).execute()
	print "completed"

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console
FLOW = OAuth2WebServerFlow(
    client_id='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    client_secret=keyring.get_password('XXXXXXX', 'XXXXXXX'),
    scope='https://www.googleapis.com/auth/tasks',
    user_agent='myTasks/v1')

# To disable the local server feature, uncomment the following line:
FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage('tasks.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google APIs Console
# to get a developerKey for your own application.
service = build(serviceName='tasks', version='v1', http=http,
       developerKey=keyring.get_password('googleDevKey', 'chadblack1'))

parser = OptionParser(usage="usage: tasks [option] arg1 arg2 arg3", version="myTasks v0.2")

parser.add_option('-l', dest="list", action='store_true', default=False, help='Lists all tasks. Takes no arguments')

parser.add_option('-n', dest="new", help='Adds new task. Pass the name of the task list and the new task as arguments in double quotes. For example: tasks -n Main "Add this task to the Main list."', action='store', metavar='<ListName> <"Task"> <YYYY-MM-DD>', type='string', nargs=3)

parser.add_option('-c', dest="clear", action='store_true', default=False, help='Clears completed tasks from your lists. Takes no arguments.')

parser.add_option('-u', dest="update", help='Updates a designated task as completed. Pass the name of the list and the number of the task. The number is available by first listing tasks with the -l command. For example: tasks -u Main 1. This command would mark the first message on the Main list as completed.', action='store', metavar='<ListName> <TaskNumber>', nargs=2)

parser.add_option('-d', dest="delTask", help='Deletes a designated task. Pass the name of the list and the number of the task. The number is available by first listing tasks with the -l command. For example: tasks -d Main 1. This command would delete the first message from the Main list.', action='store', metavar='<ListName> <TaskNumber>', type="string", nargs=2)



(opts, args) = parser.parse_args()


if opts.list == True: 
	listTasks()
elif opts.new != None:
	newTask(opts.new)
elif opts.clear == True:
	clearTask()
elif opts.update != None:
	updateTask(opts.update)
elif opts.delTask != None: 
	delTask(opts.delTask)



