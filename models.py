from google.appengine.ext import ndb


class Message(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    message = ndb.TextProperty()
    time_date = ndb.DateTimeProperty(auto_now_add=True)
