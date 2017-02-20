import webapp2

class Index(webapp2.RequestHandler):
  def get(self):
    HTML = open('index.html').read()
    self.response.out.write(HTML)

class Blog(webapp2.RequestHandler):
  def get(self):
    HTML = open('blog-post-pages/blog0.html').read()
    self.response.out.write(HTML)

class BlogPost(webapp2.RequestHandler):
  def get(self,name):
    HTML = open('blog-posts/%s.html' % name).read()
    print "hello"
    self.response.out.write(HTML)

class Blog2(webapp2.RequestHandler):
  def get(self,i):
    fname = 'blog-post-pages/blog' + str(i) + '.html'
    HTML = open(fname).read()
    self.response.out.write(HTML)

application = webapp2.WSGIApplication([
    (r'/', Index),
    (r'/blog', Blog),
    (r'/blog/(\d+)', Blog2),
    (r'/blog/(.+)', BlogPost),
], debug=True)
