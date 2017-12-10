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
import codecs

form ='''<!doctype html>
<html>
  
  <head>
    <title>Rot13</title>
    <style>
      body{
        text-align: center;
        font-size: 40px;
      }
    </style>
  </head>
  
  <body>
    <h1>Rot13</h1>
    <p>%(text1)s</p>
    <form method="post">
      <textarea name="text" rows="7" cols="60">%(text2)s</textarea>
      <br />
      <input type="submit" value="Convert">
    </form>
  </body>
  
</html>'''

def rot13Convert(s):
   return cgi.escape(codecs.encode(s, "rot-13"));

class MainPage(webapp2.RequestHandler):
   def write_form(self, text1="", text2="", textTest=False):
      if textTest:
         self.response.headers['Content-Type'] = 'text/plain';
      self.response.write(
         form%{
            'text1'  :text1,
            'text2'  :text2,
         });
   def get(self):
      self.write_form()
   def post(self):
      text_raw  = self.request.get('text');
      text_conv = rot13Convert( text_raw );
      self.write_form( text1=text_conv, text2=text_raw);

app = webapp2.WSGIApplication([
      ('/', MainPage),
   ], debug=True)

