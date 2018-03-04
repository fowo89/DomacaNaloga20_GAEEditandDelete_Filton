#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import Message

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class ResultHandler(BaseHandler):
    def post(self):
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        email = self.request.get("email")
        message = self.request.get("message")

        result = Message(first_name=first_name, last_name=last_name, email=email, message=message)
        result.put()
        """return self.write(result)"""
        self.redirect_to("list")

class ListHandler(BaseHandler):
    def get(self):
        list_ = Message.query(Message.deleted == False).fetch()
        params = {"list_": list_}
        return self.render_template("list.html", params=params)

class ListEditHandler(BaseHandler):
    def get(self, message_id):
        result = Message.get_by_id(int(message_id))

        params = {"result": result}
        return self.render_template("list_edit.html", params=params)

    def post(self, message_id):
        result = Message.get_by_id(int(message_id))
        result.message = self.request.get("new_text")
        result.put()
        return self.redirect_to("list")

class ListDeleteHandler(BaseHandler):
    def get(self, message_id):
        result = Message.get_by_id(int(message_id))

        params = {"result": result}
        return self.render_template("list_delete.html", params=params)

    def post(self, message_id):
        result = Message.get_by_id(int(message_id))
        result.deleted = True
        result.put()
        return self.redirect_to("list")

class DeletedListHandler(BaseHandler):
    def get(self):
        list_ = Message.query(Message.deleted == True).fetch()
        params = {"list_": list_}
        return self.render_template("deleted_list.html", params=params)

class DeletedListRecoverHandler(BaseHandler):
    def get(self, message_id):
        result = Message.get_by_id(int(message_id))

        params = {"result": result}
        return self.render_template("list_recover.html", params=params)

    def post(self, message_id):
        result = Message.get_by_id(int(message_id))
        result.deleted = False
        result.put()
        return self.redirect_to("deleted_list")

class DeletedListDeleteHandler(BaseHandler):
    def get(self, message_id):
        result = Message.get_by_id(int(message_id))

        params = {"result": result}
        return self.render_template("list_delete_final.html", params=params)

    def post(self, message_id):
        result = Message.get_by_id(int(message_id))
        result.key.delete()
        return self.redirect_to("deleted_list")




app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/result', ResultHandler),
    webapp2.Route('/list', ListHandler, name="list"),
    webapp2.Route('/list/<message_id:\d+>/edit', ListEditHandler),
    webapp2.Route('/list/<message_id:\d+>/delete', ListDeleteHandler),
    webapp2.Route('/deleted_list', DeletedListHandler, name="deleted_list"),
    webapp2.Route('/list/<message_id:\d+>/list_delete_final', DeletedListDeleteHandler),
    webapp2.Route('/list/<message_id:\d+>/list_recover', DeletedListRecoverHandler),
], debug=True)
