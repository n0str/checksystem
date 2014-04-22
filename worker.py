# -*- coding: utf-8 -*-
from settings import queues_names


# Назначение класса -- принять флаг, команду, сервис и положить в нужную очередь
class Worker:
    def __init__(self, queue_name):
        pass  # инициализация очереди RabbitMQ

    def push(self, team, service, flag, old_flag):
        pass # сложить все это в очередь queue_name


def init():
    for queue in queues_names:
        workers.append(Worker(queue))

workers = []
init()