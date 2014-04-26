import httplib2
import json
import os
import random
import string
import sys
import time

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# errors: (1,"sys.argv"),(2,"service unvailable"),(3,"Flag not found"),(4,"mumbled")

status = {
	"error" : [],
	"get" : 1,
	"put" : 1,
	"info" : "none",
}

def put_flag(ip, flag):
	user = id_generator()
	h = httplib2.Http(timeout=3)
	string_reg = "http://" + ip + "/1.php?registration=1&user=" + user
	string_put = "http://" + ip + "/1.php?put=1&user=" + user + "&flag=" + flag
	try:
		header, content = h.request(string_reg)
		if not user in content:
			status["error"].append(4)
			return False
		header, content = h.request(string_put)
		if "done" in content:
			return user
		else:
			status["error"].append(4)
			return False
	except:
		status["get"] = "0"
		status["error"].append(2)
		return False

def check_flag(ip, flag, info):
	h = httplib2.Http(timeout=3)
	string = "http://" + ip + "/1.php?get=1&user=" + info
	try:
		header, content = h.request(string)
		if flag in content:
			return True
		else:
			status["error"].append(3)
			return False
	except:
		status["get"] = "0"
		status["error"].append(2)
		return False

if not len(sys.argv) == 5:
	print json.dumps(
		{
			"error" : [1,],
		}
	)
	sys.exit()

ip = sys.argv[1]
flag = sys.argv[2]
info = sys.argv[3]
old_flag = sys.argv[4]

res1 = check_flag(ip,old_flag,info)
res2 = put_flag(ip,flag)

if res1 == False:
	status["get"] = 0
if res2 == False:
	status["put"] = 0
else:
	status["info"] = res2

print json.dumps(status)