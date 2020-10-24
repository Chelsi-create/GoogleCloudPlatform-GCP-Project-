import webapp2
from model import Employee
import jinja2
import os
import base64
import cloudstorage
from google.appengine.api import app_identity

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)



class MainHandler(webapp2.RequestHandler):
    'to handle a web request and response'
    def get(self):
        html = open("header.html").read()
        #writing html on web browser
        self.response.write(html)
        #writing html on web browser
        html = open("addemp.html").read()
        self.response.write(html)

class AddEmp(webapp2.RequestHandler):
    'to add new employee info from web browser'
    def post(self):
        #getting web request data from web browser
        name = self.request.POST.get("tfName")
        pin = self.request.POST.get("pfPass")
        gen = self.request.POST.get("gen")
        branch = self.request.POST.get("ddBranch")
        salary = self.request.POST.get("numESalary")
        #reading data of all image files on web browser
        files = self.request.POST.getall("profile")

        for item in files:
            self.response.write("<h3>"+item.filename+"</h3>")
            self.response.write("<h3>"+item.type+"</h3>")
            #converting image file into base64
            b64 = base64.b64encode(item.file.read())
            self.response.write("<img src = 'data:image/jpg;base64,"+b64+"' width = '300px' height = '300px'/>")
            self.response.write("</hr>")


        #Sending data on web browser
        self.response.write("<h3>"+name+"</h3>")
        self.response.write("<h3>"+pin+"</h3>")
        self.response.write("<h3>"+gen+"</h3>")
        self.response.write("<h3>"+branch+"</h3>")
        self.response.write("<h3>"+salary+"</h3>")

        #creating object of employee class
        emp = Employee()
        emp.EName = name
        emp.EPIN = int(pin)
        emp.Gen = gen
        emp.EBranch = branch
        emp.ESalary = float(salary)
        #putting employee details on database
        key = emp.put()
        self.response.write("<h3>"+str(key)+"</h3>")

class Target(webapp2.RequestHandler):
    def get(self):
        #reading from data
        name = self.request.get("tfname")
        pas = self.request.get("pfpass")
        gen = self.request.get("gen")
        # sending values to web browser
        self.response.write("<h3>"+name+"</h3>")
        self.response.write("<h3>"+pas+"</h3>")
        self.response.write("<h3>"+gen+"</h3>")   

class viewEmp(webapp2.RequestHandler):
    def get(self):
        html = open("header.html").read()
        self.response.write(html)
        #retrieving all records of database
        result = Employee.query()
        #creating a dict to load result
        template_values = {'data':result}
        #retrieving a template to render
        template = JINJA_ENVIRONMENT.get_template("viewemp.html")
        #rendering data into html
        html = template.render(template_values)
        #sending data on web browser
        self.response.write(html)

class searchEmp(webapp2.RequestHandler):
    def get(self):
        #retrieving all records of database
        result = Employee.query(Employee.EName=="chelsi Jain") 
        self.response.write("<table border = '1'>")
        self.response.write("<tr>")
        self.response.write("<th>Name</th>")
        self.response.write("<th>PIN</th>")
        self.response.write("<th>Gender</th>")
        self.response.write("<th>Branch</th>")
        self.response.write("<th>Salary</th>")
        self.response.write("<tr>")
        
        for item in result:
            self.response.write("<tr>")
            self.response.write("<td>"+item.EName+"</td>")
            self.response.write("<td>"+str(item.EPIN)+"</td>")
            self.response.write("<td>"+item.Gen+"</td>")
            self.response.write("<td>"+item.EBranch+"</td>")
            self.response.write("<td>"+str(item.ESalary)+"</td>")
            self.response.write("</tr>")
        self.response.write("</table>")
class Cloud(webapp2.RequestHandler):
    'to use cloud storage functions'
    def get(self):
        self.response.write("<h3>Google Cloud Storage</h3>")
        #retrieving default bucket name of an application
        bucket = app_identity.get_default_gcs_bucket_name()
        self.response.write("<h3>Bucket name"+bucket+"</h3>")
        #accessing all files into a bucket
        files = cloudstorage.listbucket("/"+bucket+"/")
        for file in files:
            self.response.write("<h3>"+file.filename+"</h3>")
        
        #creating file on cloud storage
        


start = webapp2.WSGIApplication([
    ('/',MainHandler),
    ('/formtarget', Target),
    ('/addemp', AddEmp),
    ('/viewemp', viewEmp),
    ('/searchemp',searchEmp),
    ('/cloudstorage',Cloud)
],debug = True)


