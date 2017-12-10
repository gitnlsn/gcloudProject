# Copyright 2016 Google Inc.
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
import cgi
import webapp2
import re

form ='''<!doctype html>
<html>
  <head>
    
    <title>Sign Up</title>
    <meta name='viewport' content="width=device-width, user-scalable=no">
    
    <style>
      body{
        text-align: center;
        font-size: 40px;
      }
      .alert{
         color: red;
      }
    </style>
    
  </head>
  
  <body>
    <h1>Sign Up</h1>
    <form method="post">
      
      <label>Userame:
         <input type="text" name="username"      value="%(username)s">        <span class='alert'>%(username_check_alert)s</span>
      </label><br />
      
      <label>Password:
         <input type="password" name="password"  value="%(password_trial)s">  <span class='alert'>%(password_check_alert)s</span>
      </label><br />
      
      <label>Password verify:
         <input type="password" name="verify"    value="%(password_verify)s"> <span class='alert'>%(password_verif_alert)s</span>
      </label><br />
      
      <label>email:
         <input type="text" name="email"         value="%(email)s">           <span class='alert'>%(email_check_alert)s</span>
      </label><br />
      
      <input type="submit">
      
    </form>
  </body>
  
</html>'''

usernameREGEX = re.compile("^[a-zA-Z0-9_-]{3,20}$");
PasswordREGEX = re.compile("^.{3,20}$");
emailREGEX    = re.compile("^[\S]+@[\S]+.[\S]+$");

def check_username(username=None):
   if username and usernameREGEX.match(username):
      return True;
   return False;

def check_password(password_trial=None):
   if password_trial and PasswordREGEX.match(password_trial):
      return True;
   return False;

def verify_Password(password_trial=None, password_verify=None):
   if password_verify and password_trial and password_trial==password_verify:
      return True;
   return False;

def check_email(email=None):
   if email and emailREGEX.match(email):
      return True;
   return False;

def escape_html(s):
   return cgi.escape(s, quote=True);

class MainPage(webapp2.RequestHandler):
   def set_userProp(username, password, email):
      self.username = username;
      self.password = password;
      self.email    = email;
   def write_form(   self, test=False,
                     username="",           password_trial="",     password_verify="",    email="",
                     username_check_msg="", password_check_msg="", password_verif_msg="", email_check_msg="",
                  ):
      if test:
         self.response.headers['Content-Type'] = 'text/plain';
      self.response.write(
      form%{
         'username'        :escape_html(username         ),
         'password_trial'  :escape_html(password_trial   ),
         'password_verify' :escape_html(password_verify  ),
         'email'           :escape_html(email            ),
         'username_check_alert' :username_check_msg,
         'password_check_alert' :password_check_msg,
         'password_verif_alert' :password_verif_msg,
         'email_check_alert'    :email_check_msg,
      });
   def get(self):
      self.write_form( );
   def post(self):
      username_req          = self.request.get("username" );
      password_trial_req    = self.request.get("password" );
      password_verify_req   = self.request.get("verify"   );
      email_req             = self.request.get("email"    );
      # username_req          = "nelson";
      # password_trial_req    = "test";
      # password_verify_req   = "test";
      # email_req             = "test";
      username_check  = check_username (username_req                             );
      password_check  = check_password (password_trial_req                       );
      password_verify = verify_Password(password_trial_req, password_verify_req  );
      email_check     = check_email    (email_req                                );
      username_check_msg  = "";
      password_check_msg  = "";
      password_verif_msg  = "";
      email_check_msg     = "";
      print username_check, password_check, password_verify, email_check;
      if not username_check:
         username_check_msg = "Username not valid";
      if not password_check:
         password_check_msg = "Password not valid";
      if not password_verify:
         password_verif_msg = "Passwords don't match";
      if not email_check:
         email_check_msg    = "E-mail not valid";
      if (username_check and password_verify and password_check and email_check):
         self.redirect("/welcome?username="+username_req);
      else:
         self.write_form( test=False,
               username=username_req,                    password_trial=password_trial_req,
               password_verify=password_verify_req,      email=email_req,
               username_check_msg=username_check_msg, password_check_msg=password_check_msg,
               password_verif_msg=password_verif_msg, email_check_msg=email_check_msg,
         );

class successLogin_Page(webapp2.RequestHandler):
   def get(self):
      # self.response.headers['Content-Type'] = 'text/plain';
      username_req = self.request.get("username");
      self.response.write("Welcome, "+username_req+"!");
      # self.response.write(self.request);

app = webapp2.WSGIApplication([
      ('/',        MainPage         ),
      ('/welcome', successLogin_Page),
   ], debug=True)

# MainPage().post()