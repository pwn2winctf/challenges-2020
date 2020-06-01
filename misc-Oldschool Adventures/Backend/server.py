#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, subprocess
import thread
import random
import string
import json
from socket import *

HOST = "0.0.0.0"
PORT = 31337
BUFF = 132
PATH = "/home/mainframe/stuff"
WEBPATH = "/var/www/html/proc/"
IP_EMULATOR = subprocess.check_output("hostname -I".split()).split()[0]

def check_pow(solution, randomstr):
	FNULL = open(os.devnull, 'w')
	return subprocess.call(["hashcash", "-cdb25", "-r", randomstr, solution], cwd="/tmp", stdout=FNULL, stderr=subprocess.STDOUT) == 0

def createName():
	name = "".join(random.sample(string.printable[:26], 10))
	return name

def createString():
	return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
	
def publishFile(name, IP):
	os.system("cp " + PATH + "/processing/" + IP + "/" + name + ".bas " + WEBPATH)
	
def readImg(name, IP):
	os.chdir(PATH)
	cmd = "./ReadBarcode " + PATH + "/done/" + IP + "/" + name + ".png"
	output = subprocess.check_output(cmd.split())
	try:
		if output.split("\r\n")[3].split()[1] == "QR_CODE":
			result = " ".join(output.split("\r\n")[4].split()[1:])
			return result
	except:
		return False
			
def executeCmd(cmd):
	os.chdir(PATH + "/secret")
	try:
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		result = p.communicate()[0]
		return result
	except:
		return False

def finishJob(name, IP):
	# soh vou manter os .bas no processing pra analise pos-CTF, na pasta funfou
	os.system("rm " + PATH + "/processing/" + IP + "/" + name + ".png")
	os.system("rm " + PATH + "/done/" + IP + "/" + name + ".png")
	os.system("rm " + WEBPATH + "/" + name + ".bas")
	#template folder
	os.system("rm -rf " + PATH + "/processing/" + IP + "/" + name + "-template")
	#se nao funfou, apagar .bas
	if os.path.exists(PATH + "/processing/" + IP + "/" + name + ".bas"):
		os.system("rm " + PATH + "/processing/" + IP + "/" + name + ".bas")

def createFiletoSend(name, IP, payload):
	file = open(PATH + "/processing/" + IP + "/" + name + ".bas", "w+")
	file.writelines(payload)
	file.close()
	
def takeScreenshot(name, IP):
	os.system("cp -r " + PATH + "/template/ " + PATH + "/processing/" + IP + "/" + name + "-template")
	os.chdir(PATH + "/processing/" + IP + "/" + name + "-template")
	
	new_fixture = {
		"url" : "jsbeeb/?autorun&loadBasic=http://" + IP_EMULATOR + "/proc/" + name + ".bas",
		"output": "saida"
	}
	
	with open("cypress/fixtures/data.json", "w") as json_file:
		json.dump(new_fixture, json_file)
	
	os.system("npm start")
	os.system("mv cypress/screenshots/print.js/saida.png " + PATH + "/processing/" + IP + "/" + name + ".png")

def changeColors(name, IP):
	os.system("convert " + PATH + "/processing/" + IP + "/" + name + ".png -colorspace HSI -separate +channel \( -clone 2 -negate \) \( -clone 1 -threshold 1% -negate \) \( -clone 2 -clone 3 -clone 4 -compose over -composite \) -delete 3,4 +swap +delete -set colorspace HSI -combine -colorspace sRGB " + PATH + "/done/" + IP + "/" + name + ".png")
	
def manipulador(clientsock, addr):

	try:
		clientsock.settimeout(60)
		randomstr = createString()
		clientsock.send("Send the solution for \"hashcash -mb 25 " + randomstr + "\": ")
		solution = clientsock.recv(BUFF)
		
		if not check_pow(solution.strip(), randomstr):
			clientsock.send("\nInvalid PoW.\n")
			clientsock.close()
			return
		
		try:
			clientsock.settimeout(5)
			clientsock.send("Send your payload here: ")
			payload = clientsock.recv(BUFF).strip()
			clientsock.send("\nWait, processing...\n")
			IP = addr[0]
			name = createName()
			if os.path.exists(PATH + "/processing/" + IP) == False:
				os.system("mkdir " + PATH + "/processing/" + IP)
				os.system("mkdir " + PATH + "/done/" + IP)
			createFiletoSend(name, IP, payload)
			publishFile(name, IP)
			takeScreenshot(name, IP)
			changeColors(name, IP)
			cmd = readImg(name, IP)
			if cmd:
				result = executeCmd(cmd)
				if result:
					if os.path.exists(PATH + "/funfou/" + IP) == False:
						os.system("mkdir " + PATH + "/funfou/" + IP)
					os.system("mv " + PATH + "/processing/" + IP + "/" + name + ".bas " + PATH + "/funfou/" + IP)
					clientsock.send(result)
				else:
					clientsock.send("\nInvalid command: " + cmd + "\n")
			else:
				clientsock.send("\nNot a valid QR!\n")
		
			finishJob(name, IP)
			clientsock.close()
			return
		
		except timeout:
			clientsock.send("\nTimeout!\n")
			clientsock.close()
			return
		
	# timeout do hashcash	
	except timeout:
		clientsock.send("\nTime limit exceeded for PoW!\n")
		clientsock.close()
		return

if __name__=='__main__':
	ADDR = (HOST, PORT)
	serversock = socket(AF_INET, SOCK_STREAM)
	serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serversock.bind(ADDR)
	serversock.listen(1)
	while 1:
		clientsock, addr = serversock.accept()
		thread.start_new_thread(manipulador, (clientsock, addr))
		
		
		