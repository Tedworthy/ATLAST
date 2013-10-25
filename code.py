import web
from dbbackend import query

render = web.template.render('templates/')

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
   # currently it runs everything as root which is LOLZ 
    return logic_to_translate;

if __name__ == "__main__":
  app = web.application(urls, globals())
  app.run()

