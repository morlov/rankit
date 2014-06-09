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
	user_name = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email    = db.StringProperty(required = True)

class Ranking(db.Model):
	user_name  = db.StringProperty(required = True)
	ranking_name = db.StringProperty(required = True)
	item_name = db.StringProperty(required = True)
	rank  = db.StringProperty(required = True)

class Item(db.Model):
	item_name    = db.StringProperty(required = True)
	content = db.StringProperty(required = True)

class Handler(webapp2.RequestHandler):
    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        temp = jinja_env.get_template(template)
        return temp.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Main(Handler):

    def get(self):
        user_name = self.request.cookies.get('user_name')
        if not user_name:
            self.redirect("/signup")
        self.render_main()

    def render_main(self):
        #posts = db.GqlQuery("select * from Post order by created desc")        
        #self.render("blog.html", posts=posts)
        user_name = self.request.cookies.get('user_name').split('|')[0]
        self.render('main.html', user_name=user_name)

class New(Handler):

    def get(self):
    	user_name = self.request.cookies.get('user_name').split('|')[0]
        self.render("new.html",user_name=user_name)

class Sort(Handler):

    def get(self):
    	user_name = self.request.cookies.get('user_name').split('|')[0]
        self.render("sort.html", user_name=user_name)

USER_RE   = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE   = re.compile(r"^.{3,20}$")
EMAIL_RE  = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_user_name(user_name):
    return user_name and USER_RE.match(user_name)
def valid_password(password):
    return password and PASS_RE.match(password)
def valid_email(email):
    return email and EMAIL_RE.match(email)

def valid_signup(self, email, password, verify, user_name, user):
    if not valid_email(email):
        return "That's not a valid email."
    if not valid_password(password):
        return "That's a valid password."
    if password != verify:
        return "Your passwords didn't match."
    if not valid_user_name(user_name):
        return "That's not a valid username."
    if user:
        return "This user already exists."

class Signup(Handler):

    def get(self):
        self.render("signup.html")

    def post(self):
        
        user_name = self.request.get('user_name')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        user = db.GqlQuery("SELECT * FROM User WHERE user_name=:user_name", user_name=user_name).get()

        error_login = valid_signup(self, email, password, verify, user_name, user)
        if error_login:
            self.render('signup.html', error_login=error_login, email=email, password=password, verify=verify, user_name=user_name,user=user)
        else:
            User(user_name=user_name, email=email, password=password).put()
            h = make_secure_val(user_name)
            self.response.headers.add_header('Set-Cookie', 'user_name=%s; Path=/' % str(h))
            self.redirect('/')

class Signin(Handler):

    def get(self):
        user_name = self.request.cookies.get('user_name')
        if not user_name:
            self.render('signin.html')
        else:
            self.redirect('/')

    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')
        user = db.GqlQuery("SELECT * FROM User WHERE email=:email",email=email).get()
        user_name = user.user_name;

        if (not user) or (password != user.password):
            self.render('signin.html', error_login = "Invalid mail or password.", email=email, password=password)
        else:
            h = make_secure_val(user_name)
            self.response.headers.add_header('Set-Cookie', 'user_name=%s; Path=/' % str(h))
            self.redirect('/')

class Signout(Handler):

    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user_name=;Path=/')
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/',        Main),
    ('/new',     New),
    ('/sort',    Sort),
    ('/signup',  Signup),
    ('/signin',  Signin),
    ('/signout', Signout)
    ], debug=True)
