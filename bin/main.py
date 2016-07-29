import tornado.ioloop

from urls import patterns,settings

application = tornado.web.Application(patterns, **settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()