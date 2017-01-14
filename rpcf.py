#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, threading, time, requests, re, operator, json, subprocess
from flask import Flask, render_template, request
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))
import RPi.GPIO as GPIO

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

servoCenter = 59
servoLeft = 75
servoLeftR = servoLeft-servoCenter
servoRight = 33
servoRightR = servoRight-servoCenter
def setServo():
	val = 0
	if servoStyr == 0:
		val = 59
	if servoStyr > 0 :
		val = 59+(servoRightR/100.0)*servoStyr
	if servoStyr < 0 :
		val = 59+(servoLeftR/100.0)*-servoStyr
	#print(val)
	os.system("echo 0=%s%% > /dev/servoblaster" % val)

motorFrontF = 36
motorFrontB = 35
motorBackF = 38
motorBackB = 37
def setDrive():
	val = 0
	if motorDrive == 0:
		GPIO.output(motorFrontF, GPIO.LOW)
		GPIO.output(motorFrontB, GPIO.LOW)
		GPIO.output(motorBackF, GPIO.LOW)
		GPIO.output(motorBackB, GPIO.LOW)
	if motorDrive > 0 :
		GPIO.output(motorFrontF, GPIO.HIGH)
		GPIO.output(motorFrontB, GPIO.LOW)
		GPIO.output(motorBackF, GPIO.HIGH)
		GPIO.output(motorBackB, GPIO.LOW)
	if motorDrive < 0 :
		GPIO.output(motorFrontF, GPIO.LOW)
		GPIO.output(motorFrontB, GPIO.HIGH)
		GPIO.output(motorBackF, GPIO.LOW)
		GPIO.output(motorBackB, GPIO.HIGH)

def playLoop():
	processWhile = None
	while 1:
		#print("motorDrive: %s" % motorDrive)
		#print("servoStyr: %s" % servoStyr)
		setServo()
		setDrive()
		time.sleep(0.1)

if __name__ == '__main__':
	global flaskThread

	print("Starting servoblaster")
	#os.system("sudo /home/pi/PiBits/ServoBlaster/user/servod --p1pins=11")

	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	GPIO.setup(motorFrontF, GPIO.OUT)
	GPIO.setup(motorFrontB, GPIO.OUT)
	GPIO.setup(motorBackF, GPIO.OUT)
	GPIO.setup(motorBackB, GPIO.OUT)

	print("Starting webserver..")
	flaskThread = threading.Thread(target=flaskApp.run, kwargs={'host': '0.0.0.0', 'port': 8080, 'use_reloader':False, 'debug': True})
	flaskThread.start()

	print("Starting play loop")
	playThread = threading.Thread(target=playLoop, args=())
	playThread.start()


