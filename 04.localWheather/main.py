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

html_page ='''<!DOCTYPE html>
<html>
  <head>
    <title>Local Weather</title>
    <meta charset='UTF-8'/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <style>
      body{
        text-align: center;
        font-size: 40px;
      }
    </style>
    <script>
      var is_celcius = true;
      function update_location(){
        console.log("funciton udpate_location: started");
        $.getJSON("https://freegeoip.net/json/", function(location_response){
          console.log("funciton udpate_location: got coordinantes");
          console.log(location_response);
          $("#physical_location").html( "<p>Location: "+location_response.country_name+", "+location_response.region_code+", "+location_response.city+" ("+location_response.ip+")</p>" );
          $("#local_coordinates").html("<p>latitude: "+location_response.latitude+" deg</br>longitude: "+location_response.longitude+" deg</p>");
          $.ajax({
            url: "https://fcc-weather-api.glitch.me/api/current?lat="+location_response.latitude+"&lon="+location_response.longitude,
            dataType: "json",
            success: function(weather_response){
              console.log("funciton udpate_location: got weather");
              console.log(weather_response);
              if (is_celcius){
                $("#temperature").html("<p>Temperature: "+weather_response.main.temp+" degC </br>Weather: "+weather_response.weather[0].main+"<img src='"+weather_response.weather[0].icon+"'></p>");
                is_celcius = false;
              }
              else{
                $("#temperature").html("<p>Temperature: "+weather_response.main.temp*1.8+32+" degF </br>Weather: "+weather_response.weather[0].main+"<img src='"+weather_response.weather[0].icon+"'></p>");
                is_celcius = true;
              }
              console.log(weather_response.weather[0].icon);
            }, // end - ajax success function
          });
        }); // end - getJSON success function
        console.log("udpate_location: finished.");
      } // end - update_location
      $(document).ready(function(){
        console.log("document ready");
        update_location();
      });
    </script>
  </head>
  <body>
    <h1>Local Weather Machine</h1>
    <p id="physical_location">loading</p>
    <p id="local_coordinates"></p>
    <p id="temperature"><img id="weather_image" src=""></p>
    <button onclick="update_location()">Change!</button>
  </body>
</html>'''

class MainPage(webapp2.RequestHandler):
   def get(self):
      self.response.write(html_page);

app = webapp2.WSGIApplication([
      ('/', MainPage),
   ], debug=True)

