import web
import os
import parsing.parser
from celery import Celery
from dbbackend import query

render = web.template.render('templates/')
celery = Celery('code',backend='amqp',broker='amqp://guest@localhost//')

urls = (
  '/', 'index'
)

logic_form = web.form.Form(
    web.form.Textarea('logic', class_="box_sizing")
)

class index:
  def GET(self):
    form = logic_form()
    return render.index(form);

  def POST(self):
    form = logic_form()
    # Validates the Form
    form.validates()
    # TODO: We have the logic as a string, we need to process it
    logic_to_translate = form.logic.get_value()
   # translated = query.query(logic_to_translate) TODO secure the connection, 
   # currently it runs everything as root which is LOLZ i
    web.header('Content-Type','text/html; charset=utf-8', unique=True) 
    result = parseQ(logic_to_translate)
    print result.ready()
    return logic_to_translate;


def is_test():
    if 'WEBPY_ENV' is os.environ:
        return os.environ['WEBPY_ENV'] == 'test'

app = web.application(urls, globals())

if (not is_test()) and  __name__ == "__main__":
  app.run()




@celery.task
def parseQ(input):
	return parsing.parser.dat_parsing(input);
