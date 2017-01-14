#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, threading, time, requests, re, operator, json, subprocess
from flask import Flask, render_template, request
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

flaskThread = None
flaskApp = Flask(__name__)
playThread = None

motorDrive = 0
servoStyr = 0

def validateIntInput(input):
	try:
		input = int(input)
		if input <= 100 and input >= -100:
			return True
		else:
			return False
	except:
		return False

def handleCommads(args):
	global motorDrive, servoStyr
	for arg in args:
		value = args.get(arg)
		if arg == "motorDrive":
			if validateIntInput(value):
				motorDrive = int(value)
		if arg == "servoStyr":
			if validateIntInput(value):
				servoStyr = int(value)

@flaskApp.route("/")
def defaultRoute():
	handleCommads(request.args)
	template = env.get_template('basetemplate.html')
	templateValues = {
		'motorDrive' : motorDrive,
		'servoStyr' : servoStyr
    }
	return template.render(templateValues)

def playLoop():
	processWhile = None
	while 1:
		print("motorDrive: %s" % motorDrive)
		print("servoStyr: %s" % servoStyr)
		time.sleep(1)

if __name__ == '__main__':
	global flaskThread

	print("Starting webserver..")
	flaskThread = threading.Thread(target=flaskApp.run, kwargs={'host': '0.0.0.0', 'port': 8080, 'use_reloader':False, 'debug': True})
	flaskThread.start()

	print("Starting play loop")
	playThread = threading.Thread(target=playLoop, args=())
	playThread.start()


