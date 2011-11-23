#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import gflags
import httplib2
import keyring
import sys
import datetime



from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

def today():
	return todayDate.isoformat()

def tomorrow():
	return (todayDate + datetime.timedelta(days=1)).isoformat()

def nextWeek():
	return (todayDate + datetime.timedelta(days=7)).isoformat()

def nextMonth():
	return (todayDate + datetime.timedelta(days=30)).isoformat()	

def dueDate(due):
	due = due.lower()
	if weekdays.has_key(due) and weekdays[due] > todayDate.isoweekday(): 
		diff = weekdays[due] - todayDate.isoweekday()
		dueDate = (todayDate + datetime.timedelta(diff)).isoformat()
	elif weekdays.has_key(due) and weekdays[due] <= todayDate.isoweekday():
		diff = 6 - todayDate.isoweekday()
		dueDate = (todayDate + datetime.timedelta(diff)).isoformat()
	elif relDays.has_key(due):	    
		dueDate = relDays[due]()
	else: 
		dueDate = due
	return dueDate+'T12:00:00.000Z'

def tasks(listID):
	tasks = service.tasks().list(tasklist=listID).execute()
	n=1
	try: 
		for task in tasks['items']:
			if task['title'] == '': pass
			else:
				taskName=tasks['title']
				dueDate='No date.'
				if 'due' in task: 
					fullDueDate=str(task['due'])
					dueDate=fullDueDate[:10]
				
				if 'parent' in task.keys():
					task['taskNum'] = n					
					print '       '+str(task['taskNum'])+'. '+task['title'].encode('utf-8', 'ignore')+' : '+dueDate
					n+=1
				else: 
					task['taskNum'] = n
					print '    '+str(n)+'. '+task['title'].encode('utf-8', 'ignore')+' : '+dueDate
					n += 1
	except KeyError: print '    No tasks.'

def listTasks(listName, tasklists):
	if listName == []:
		for tasklist in tasklists['items']:
			print tasklist['title']
			listID=tasklist['id']
			tasks(listID)					
			print
	else:
		for tasklist in tasklists['items']:
			if tasklist['title'] != listName[0]: pass
			else:
				print tasklist['title']
				listID=tasklist['id']
				tasks(listID)
		

def renameList(opts, tasklists):
	origList = opts[0]
	newList = opts[1]
	for tasklist in tasklists['items']:
		if tasklist['title'] == origList:
			tasklist['title'] = newList
			result = service.tasklists().update(tasklist=tasklist['id'], body=tasklist).execute()
			print origList+' renamed '+newList
			break

def delList(opts, tasklists):
	listName = opts
	for tasklist in tasklists['items']:
		if tasklist['title'] == listName[0]:
			service.tasklists().delete(tasklist=tasklist['id']).execute()
			print listName, " deleted!"
			break		

def newTask(opts, tasklists):
	listName = opts[0]
#	dueDate = ''
	if len(opts) > 2:
#		if opts[2] == 'today':
#			dueDate = today.strftime('%Y-%m-%d')
#		elif opts[2] == 'tomorrow':
#			dueDate = tomorrow.strftime('%Y-%m-%d')
#		elif opts[2] == 'next week':
#			dueDate = nextWeek.strftime('%Y-%m-%d')
#		elif opts[2] == '2 weeks':
#			dueDate = twoWeeks.strftime('%Y-%m-%d')
#		elif opts[2] == 'next month':
#			dueDate = nextMonth.strftime('%Y-%m-%d')
#		else: dueDate = opts[2]
#		convertDue = dueDate+'T12:00:00.000Z'
		convertDue = dueDate(opts[2])
		task = {
	 		'title': opts[1], 
	 		'due': convertDue,
			}
	else:
		task = {
			'title': opts[1]
			}					
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

def clearTask(tasklists):
	for tasklist in tasklists['items']:
		listID = tasklist['id']
		service.tasks().clear(tasklist=listID, body='').execute()
	print 'Cleared.'

def delTask(opts, tasklists):
	listName= opts[0]
	taskNumber = int(opts[1])
    # match list off of list name
	listID = None
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

def updateTask(opts, tasklists):
	listName = opts[0]
	taskNumber = int(opts[1])		
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
	print "Completed"


relDays = {'today':today, 'tomorrow':tomorrow, 'nextWeek': nextWeek, 'nextMonth':nextMonth}

weekdays = {'mon':0, 'tue':1, 'wed':2, 'thu':3, 'fri':4, 'sat':5, 'sun':6, 'monday' : 0, 'tuesday':1, 'wednesday':2,'thursday':3, 'friday':4, 'saturday':5, 'sunday':6 }

todayDate = datetime.date.today()

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console
FLOW = OAuth2WebServerFlow(
    client_id='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    client_secret=keyring.get_password('XXXXXXX', 'XXXXXXXX'),
    scope='https://www.googleapis.com/auth/tasks',
    user_agent='myTasks/v1')

# To disable the local server feature, uncomment the following line:
FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.

taskStore = "/PATH/TO/tasks.dat"
storage = Storage(taskStore)
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http(cache=".cache")
http = credentials.authorize(http)


# Build a service object for interacting with the API. Visit
# the Google APIs Console
# to get a developerKey for your own application.
service = build(serviceName='tasks', version='v1', http=http,
       developerKey=keyring.get_password('XXXXXXXXX', 'XXXXXXXXX'))

parser = argparse.ArgumentParser(usage="tasks [option] arg1 arg2 arg3", 
	prog="myTasks v0.3")

parser.add_argument('-l', dest="tList", action='store', nargs="*", 
	help='Lists tasks. For a sinlge list, pass the list name.')

parser.add_argument('-n', dest="new", help='Adds new task. Pass the name of the task list and the \
	new task as arguments in double quotes. For example: tasks -n Main "Add this task to the Main list."', 
	action='store', metavar='<ListName> <"Task"> <YYYY-MM-DD>', nargs="*")

parser.add_argument('-c', dest="clear", action='store_true', default=False, 
	help='Clears completed tasks from your lists. Takes no arguments.')

parser.add_argument('-u', dest="update", help='Updates a designated task as completed. Pass the \
	name of the list and the number of the task. The number is available by first listing tasks \
	with the -l command. For example: tasks -u Main 1. This command would mark the first message \
	on the Main list as completed.', action='store', metavar='<ListName> <TaskNumber>', nargs="*")

parser.add_argument('-d', dest="delTask", help='Deletes a designated task. Pass the name of the list and the \
	number of the task. The number is available by first listing tasks with the -l command. \
	For example: tasks -d Main 1. This command would delete the first message from the Main list.', 
	action='store', metavar='<ListName> <TaskNumber>', nargs="*")

parser.add_argument('-R', dest="newList", help='Renames a task list. Pass the old list name and the \
	new list name. For example: tasks -R Main Home. This command would rename the Main list as the Home \
	list.', action='store', metavar='<old ListName> <new ListName>', nargs=2)

parser.add_argument('-D', dest="delList", help='Delete a task list. Pass the targeted list name. \
	For example: tasks -D Main. This command would delete the Main task list.', action='store', 
	metavar='<target listName>', nargs=1)


tasklists = service.tasklists().list().execute()
opts = parser.parse_args()


if opts.new != None:
	newTask(opts.new, tasklists)
elif opts.clear == True:
	clearTask(tasklists)
elif opts.update != None:
	updateTask(opts.update, tasklists)
elif opts.delTask != None: 
	delTask(opts.delTask, tasklists)
elif opts.newList != None:
	renameList(opts.newList, tasklists)
elif opts.delList != None:
	delList(opts.delList, tasklists)
elif opts.tList != None: 
	listTasks(opts.tList, tasklists)



