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
from subprocess import Popen, PIPE
from time import sleep


def generate_flag(team, service):
	# Добавление флага в БД
	start = (
		str(md5(str(getrandbits(128))).hexdigest()),
		str(team[0]),
		str(service[0]),
	)
	cur.execute("INSERT INTO flags VALUES (NULL,%s,%s,%s,NULL,'0000-00-00 00:00:00','0000-00-00 00:00:00')", start)
	cur.execute("INSERT INTO flags_info VALUES (%s,'')", (start[0],))
	db.commit()
	return start[0]

def get_old_flag(team, service):
	start = (
		str(team[0]),
		str(service[0]),
	)
	cur.execute("SELECT flag FROM flags WHERE team_id=%s AND service_id=%s ORDER BY post_timestamp DESC LIMIT 1",start)
	return cur.fetchall()[0][0]
	
# Дополнительная информация для проверки флага
def get_old_info(flag):
	start = (str(flag),)
	cur.execute("SELECT info FROM flags_info WHERE flag = %s LIMIT 1",start)
	return cur.fetchall()[0][0]
	
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

def start_new_round(channel_workers):
	global current_round
	current_round += 1
	flags_list = []

	for team in teams:
		for service in services:
			if current_round > 0:
				old_flag = get_old_flag(team, service)
				old_info = get_old_info(old_flag)
			else:
				old_flag = ""
				old_info = ""
			flag = generate_flag(team, service)
			flags_list.append((team, service, flag, old_flag, old_info))

	shuffle(flags_list)
	for elem in flags_list:
		team, service, flag, old_flag, old_info = elem
		push_to_worker(channel_workers, team, service, flag, old_flag, old_info)


def checker_answer_callback():
	# проверить, что все ответы за раунд пришли
	# обработать ответы, положить в базу
	# посчитать кол-во ответов за раунд, если все, то новый раунд
	# если подолшло время финиша игры, то exit
	pass


def instance_work(self_name):
	def callback(ch, method, properties, body):
		print "%s : Received %r" % (self_name, body,)
		ch.basic_ack(delivery_tag = method.delivery_tag)
	
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='task_queue', durable=True)
	channel.basic_qos(prefetch_count=1)
	channel.basic_consume(callback, queue='task_queue')
	
	if DEBUG:
		print "start #", self_name

	channel.start_consuming()

	# получит из очереди команду, сервис, флаг, старый флаг
	# вызовет 2 чекера по очереди
	# результаты работы чекеров -- в очередь answers


def init():
	connection_answer = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel_answer = connection_answer.channel()
	channel_answer.queue_declare(queue='answers')
	channel_answer.basic_consume(checker_answer_callback, queue='answers', no_ack=True)

	connection_workers = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel_workers = connection_workers.channel()
	channel_workers.queue_declare(queue='task_queue', durable=True)

	for queue in range(queue_len):
		proc = Process(target=instance_work, args=(queue, ))
		workers.append(proc)
		proc.start()

	sleep(3)
	start_new_round(channel_workers)
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


#init()

out, err = Popen('python checker.py', shell=True, stdout=PIPE).communicate()
print out
