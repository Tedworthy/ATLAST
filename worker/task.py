import sys
from celery import Celery

from ..parsing import *
celery = Celery('task', backend='amqp://guest@localhost:5672', broker='amqp://guest@localhost')

@celery.task
def add_to_parse_q(logic_to_translate):
    
    return dat_parsing(logic_to_translate)

