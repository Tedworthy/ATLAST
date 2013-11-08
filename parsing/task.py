import sys
from celery import Celery

from parser import parse_input
celery = Celery('task', backend='amqp://guest@localhost:5672', broker='amqp://guest@localhost')

@celery.task
def add_to_parse_q(logic_to_translate):
  return parse_input(logic_to_translate)

