#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import os
import jinja2
import re
import hashlib
import hmac
import json

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'html')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

secret = 'jd;d*hskJ7lsjbGSdjsLuhsnh!jusjdsklLHFs'

def make_secure_val(s):
    return "%s|%s" % (s, hmac.new(secret, s).hexdigest())

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val

class User(db.Model):
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email    = db.StringProperty(required = True)

class Handler(webapp2.RequestHandler):
    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        temp = jinja_env.get_template(template)
        return temp.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Main(Handler):

	def render_main(self):
		#posts = db.GqlQuery("select * from Post order by created desc")        
		#self.render("blog.html", posts=posts)
		username = self.request.cookies.get('username').split('|')[0]
		self.render('main.html', username=username)

	def get(self):
		username = self.request.cookies.get('username')
		if not username:
			self.redirect('/signup')
		self.render_main()

class New(Handler):

    def get(self):
        self.render("new.html")

class Sort(Handler):

    def get(self):
    	username = self.request.cookies.get('username').split('|')[0]
        self.render("sort.html", username=username)

class Signup(Handler):

    def get(self):
        self.render("signup.html")

USER_RE   = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE   = re.compile(r"^.{3,20}$")
EMAIL_RE  = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return username and USER_RE.match(username)
def valid_password(password):
    return password and PASS_RE.match(password)
def valid_email(email):
    return email and EMAIL_RE.match(email)

class Signup(Handler):

    def get(self):
        self.render("signup.html")

    def post(self):
        
        username = self.request.get('username')
        password = self.request.get('password')
        verify   = self.request.get('verify')
        email    = self.request.get('email')

        user = db.GqlQuery("SELECT * FROM User WHERE username=:username", username=username).get()

        error_login = None

        if not valid_email(email):
            error_login = "That's not a valid email."
        elif not valid_password(password):
            error_login  = "That's a valid password."
        elif password != verify:
            error_login  = "Your passwords didn't match."
        elif not valid_username(username):
            error_login = "That's not a valid username."
        elif user:
            error_login = "This user already exists." 

        if error_login:
            self.render('signup.html', error_login=error_login, email=email, password=password, verify=verify, username=username)
        else:
            u = User(username=username, email=email, password=password)
            u.put()
            h = make_secure_val(email)
            self.response.headers.add_header('Set-Cookie', 'sername=%s; Path=/' % str(h))
            self.redirect('/')

class Signin(Handler):

    def get(self):
        username = self.request.cookies.get('username')
        if not username:
            self.render('signin.html')
        else:
            self.redirect('/')

    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')
        user = db.GqlQuery("SELECT * FROM User WHERE email=:email",email=email).get()
        username = user.username;

        if (not user) or (password != user.password):
            self.render('signin.html', error_login = "Invalid mail or password.", email=email, password=password)
        else:
            h = make_secure_val(username)
            self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % str(h))
            self.redirect('/')

class Signout(Handler):

    def get(self):
        self.response.headers.add_header('Set-Cookie', 'username=;Path=/')
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/',        Main),
    ('/new',     New),
    ('/sort',    Sort),
    ('/signup',  Signup),
    ('/signin',  Signin),
    ('/signout', Signout)
    ], debug=True)
