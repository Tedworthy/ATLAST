import web


render = web.template.render('templates/')

urls = (
  '/', 'index'
)

class index:
  def GET(self):
    return render.index('Sam')

if __name__ == "__main__":
  app = web.application(urls, globals())
  app.run()

