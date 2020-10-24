from google.appengine.ext import ndb

class Employee(ndb.Model):
    'to store employee details into database'
    EName = ndb.StringProperty()
    EPIN = ndb.IntegerProperty()
    Gen = ndb.StringProperty()
    EBranch = ndb.StringProperty()
    ESalary = ndb.FloatProperty()
    EDate = ndb.DateTimeProperty(auto_now_add = True)