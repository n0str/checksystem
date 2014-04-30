import httplib2
import json
import os
import random
import string
import sys
import time
import re

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# errors: (1,"sys.argv"),(2,"service unvailable"),(3,"Flag not found"),(4,"mumbled")
headers = {
	'Content-Type':'application/x-www-form-urlencoded',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
	'Accept-Encoding': 'gzip, deflate',
	'Cookie' : '',
	'Connection': 'keep-alive'
}

status = {
	"error" : [],
	"get" : 1,
	"put" : 1,
	"info" : "none",
}


def reg_login(ip):
	string_reg = "http://" + ip + "/index.php?register=page"
	string_login = "http://" + ip + "/index.php"

	pswd = id_generator(size=random.randint(1,6))
	login = id_generator(size=random.randint(4,8))
	h = httplib2.Http(timeout=3)
	try:
		#register
		post_param = 'on_register=on&reg_login=' + login + '&password=' + pswd + '&repeat_password=' + pswd
		response, content = h.request(string_reg, 'POST', post_param, headers=headers)
		if not 'reg_ok' in response['location']:
			status["error"].append(4)
			return False
		headers['Cookie'] = response['set-cookie']

		#login
		post_param = 'login=' + login + '&password=' + pswd
		response, content = h.request(string_login, 'POST', post_param, headers=headers)
		if not 'Cash:' in content:
			status["error"].append(4)
			return False
		
		return True
	except:
		status["get"] = "0"
		status["error"].append(2)
		return False


def put_flag(ip, flag):
	string_put = "http://" + ip + "/index.php"
	
	h = httplib2.Http(timeout=3)
	try:
		#put flag
		post_param = 'on_freeze=on&text=' + flag
		response, content = h.request(string_put, 'POST', post_param, headers=headers)

		a = re.compile('\:\:\:(\w+)')
		return a.findall(content)[0] #return shield

	except:
		status["get"] = "0"
		status["error"].append(2)
		return False

def check_flag(ip, flag, info):
	string_test = "http://" + ip + "/index.php?freeze=page"
	string_check = "http://" + ip + "/index.php"
	
	h = httplib2.Http(timeout=3)
	try:
		#get list shield
		header, content = h.request(string_test, headers=headers)
		if not info in content:
			status["error"].append(3)
			return False
		a = re.compile('getText\((\d+)\);\'>' + info)
		id_shield = a.findall(content)
		
		#get flag by shield
		post_param = 'unfreeze_id=' + id_shield[-1] 
		response, content = h.request(string_check, 'POST', post_param, headers=headers)
		if content == flag:
			return True
		else:
			status["error"].append(3)
			return False
			
	except:
		status["get"] = "0"
		status["error"].append(2)
		return False

#############START####################

if 0 and not len(sys.argv) == 5:
	print json.dumps(
		{
			"error" : [1,],
		}
	)
	sys.exit()

##############SYS.ARGV###############

ip = sys.argv[1] 		#"127.0.0.1/labs/dbo/dbo_service" 
flag = sys.argv[2] 		#'RootSecret' #
info = sys.argv[3] 		#'360quivb0p' # #shield //status["info"]
old_flag = sys.argv[4] 	#'qwertyui' #

############# MAIN PROGRAM #############

login = reg_login(ip)
if login == False:
	status["get"] = 0
	status["put"] = 0
	
res1 = check_flag(ip,old_flag,info)
if res1 == False:
	status["get"] = 0

res2 = put_flag(ip,flag)
if res2 == False:
	status["put"] = 0
else:
	status["info"] = res2


print json.dumps(status)
