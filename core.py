# -*- coding: utf-8 -*-
from hashlib import md5
from random import shuffle
from multiprocessing import Process
from settings import *
from random import getrandbits
import pika
import sys
import json
import base64
import MySQLdb
import subprocess, threading
from time import sleep
from time import localtime, strftime, time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    COOL = '\033[1;32m'

# Принимает команду для запуска чекера. Возвращает stdout чекера.
# @param: timeout - таймаут чекера
class Command(object):
	def __init__(self, cmd):
		self.cmd = cmd
		self.process = None
		self.out = None

	def run(self, timeout):
		def target():
			self.process = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE)
			self.out, err = self.process.communicate()

		thread = threading.Thread(target=target)
		thread.start()

		thread.join(timeout)
		if thread.is_alive():
			print 'Terminating process by timeout'
			print >> sys.stderr, 'Terminating process by timeout at %s' % (str(time()),) 
			self.out = "timeout"
			self.process.terminate()
		return self.out

def generate_flag(team, service):
	start = (
		str(md5(str(getrandbits(128))).hexdigest()),
		str(team[0]),
		str(service[0]),
	)
	cur.execute("INSERT INTO flags VALUES (NULL,%s,%s,%s,NULL,'0000-00-00 00:00:00','-10','-10')", start)
	cur.execute("INSERT INTO flags_info VALUES (%s,'none')", (start[0],))
	db.commit()
	return start[0]

def get_old_flag(team, service):
	start = (
		str(team[0]),
		str(service[0]),
	)
	cur.execute("SELECT flag FROM flags WHERE team_id=%s AND service_id=%s ORDER BY post_timestamp DESC LIMIT 1",start)
	res = "none"
	try:
		res = cur.fetchall()[0][0]
	except:
		res = "none"
	return res
	
# Дополнительная информация для проверки флага
def get_old_info(flag):
	start = (str(flag),)
	cur.execute("SELECT info FROM flags_info WHERE flag = %s LIMIT 1",start)
	res = "none"
	try:
		res = cur.fetchall()[0][0]
	except:
		res = "none"
	return res
	
def push_to_worker(channel_workers, team, service, flag, old_flag, old_info):
	payload = json.dumps({
		'team' : team,
		'service' : service,
		'flag' : flag,
		'old_flag' : old_flag,
		'old_info' : old_info
	})
	channel_workers.basic_publish(exchange='',
		routing_key='task_queue',
		body=payload,
		properties=pika.BasicProperties(
			delivery_mode = 2, # make message persistent
		)
	)

def start_new_round():
	global current_round
	current_round += 1
	answers_dict["time"] = time()

	print  "%sCURRENT ROUND # %s at [%s]%s" % (bcolors.COOL, current_round,strftime("%Y-%m-%d %H:%M:%S", localtime()), bcolors.ENDC)

	flags_list = []

	for team in teams:
		for service in services:
			if current_round > 0:
				old_flag = get_old_flag(team, service)
				old_info = get_old_info(old_flag)
			else:
				old_flag = "none"
				old_info = "none"
			flag = generate_flag(team, service)
			flags_list.append((team, service, flag, old_flag, old_info))

	shuffle(flags_list)

	for elem in flags_list:
		team, service, flag, old_flag, old_info = elem
		push_to_worker(channel_workers, team, service, flag, old_flag, old_info)

def checker_answer_callback(ch, method, properties, body):
	ans_count = len(teams) * len(services)
	if not current_round in answers_dict:
		answers_dict[current_round] = 0
	answers_dict[current_round] += 1

	payload = json.loads(body)


	print "Received : \told_flag=%s\n\t\tflag=%s\n\t\told_info=%s\n\t\tteam=%s\n\t\tservice=%s\n\t\t---------------------" % (
		payload[0]["old_flag"], payload[0]["flag"], payload[0]["old_info"], payload[0]["team"], payload[0]["service"], 
	)

	if "checker_error" in payload[1]["error"]:
		print bcolors.FAIL + "\t\tERROR (checker timeout)" + bcolors.ENDC
	else:
		try:
			flag = payload[0]["flag"]
			#team = payload[0]["team"][0]
			#service = payload[0]["service"][0]
			info = payload[1]["info"]
			error = payload[1]["error"]
			get_result = payload[1]["get"]
			put_result = payload[1]["put"]
			start1 = (get_result, put_result, flag)
			cur.execute("UPDATE flags SET check_status=%s,put_status=%s WHERE flag=%s", start1)
			start2 = (info, flag)
			cur.execute("UPDATE flags_info SET info=%s WHERE flag=%s", start2)
			db.commit()

			print "\t\tput_result=%s\n\t\tget_result=%s\n\t\tinfo=%s\n\t\terror=%s" % (
				put_result,get_result,info,error,
			)
		except:
			print "ERROR (checker_answer_callback)"

	if ans_count == answers_dict[current_round]:
		dlt = time() - answers_dict["time"]
		if dlt < ROUND_DURATION:
			sleep(ROUND_DURATION - dlt)
		start_new_round()
		# проверка соединения	

	# если подолшло время финиша игры, то exit


def instance_work(self_name):
	def callback(ch, method, properties, body):
		payload = json.loads(body)

		string = "python %s %s %s %s %s" % (payload["service"][2], payload["team"][2], payload["flag"], payload["old_info"], payload["old_flag"])
		#print string
		command = Command(string)
		out = command.run(timeout=CHECKER_TIMEOUT)
		#out, err = subprocess.Popen(string, shell=True, stdout=subprocess.PIPE).communicate()	
		#print "%s : Received %r %s" % (self_name, body,out)

		out_payload = ""
		try:
			out_payload = json.loads(out)
		except:
			print >> sys.stderr, 'error (instance_work,callback) at %s\n%s' % (str(time()),out) 
			out_payload = {"error" : ["checker_error",],}

		sendtext = json.dumps([payload,out_payload])

		channel.basic_publish(exchange='',
                      routing_key='answers',
                      body=sendtext)

		ch.basic_ack(delivery_tag = method.delivery_tag)
	
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='task_queue', durable=True)
	channel.basic_qos(prefetch_count=1)
	channel.basic_consume(callback, queue='task_queue')
	
	if DEBUG:
		print "start #", self_name

	channel.start_consuming()

def init():
	connection_answer = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel_answer = connection_answer.channel()
	channel_answer.queue_declare(queue='answers')
	channel_answer.basic_consume(checker_answer_callback, queue='answers', no_ack=True)

	for queue in range(queue_len):
		proc = Process(target=instance_work, args=(queue, ))
		workers.append(proc)
		proc.start()

	sleep(3)
	start_new_round()
	channel_answer.start_consuming()

	connection_workers.close()
	connection_answer.close()

DEBUG = True
answers_dict = {}
workers = []
current_round = 0


db = MySQLdb.connect(host=db_settings["host"],
		user=db_settings["user"],
		passwd=db_settings["password"],
		db=db_settings["db"])
cur = db.cursor() 


connection_workers = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel_workers = connection_workers.channel()
channel_workers.queue_declare(queue='task_queue', durable=True)

init()


