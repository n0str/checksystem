# -*- coding: utf-8 -*-
from hashlib import md5
from random import shuffle
from multiprocessing import Process
from settings import *
from worker import workers


def generate_flag(team, service):
    return md5('yozik').hexdigest()

def get_old_flag(team, service):
    return md5('yozik2').hexdigest()


def start_new_round():
    current_round += 1
    flags_list = []

    for team in teams:
        for service in services:
            old_flag = get_old_flag(team, service)
            flag = generate_flag(team, service)
            flags_list.append((team, service, flag, old_flag))

    shuffle(flags_list)
    i = 0
    for elem in flags_list:
        team, service, flag, old_flag = elem
        workers[i % len(workers)].push(team, service, flag, old_flag)
        i += 1


def checker_answer_callback():
    # проверить, что все ответы за раунд пришли
    # обработать ответы, положить в базу
    # посчитать кол-во ответов за раунд, если все, то новый раунд
    # если подолшло время финиша игры, то exit
    pass


def instance_work(queque_name):
    # получит из очереди команду, сервис, флаг, старый флаг
    # вызовет 2 чекера по очереди
    # результаты работы чекеров -- в очередь answers
    pass


def init():
    # Инициализировать RabbitMQ. Создать очередь ответов и очереди с именами из queues_names
    for queue in queues_names:
        proc = Process(target=instance_work, args=(queue,))
        proc.start()

    # start_new_round
    # loop


answers_dict = {}
current_round = 0