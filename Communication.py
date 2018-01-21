"""
Project:     hw08-communication.py

Description: This program obtains weather data from Wundeground and delivers
             weather information to a user via Twilio's SMS service. It also
             recommends attire based on certain weather parameters.

Name:        Owen Wiese

Date:        November 20, 2015

Notes:       You must intall the Twilio library and the urllib2 library
             using the SSH Terminal

             sudo pip install urllib2
             sudo pip install twilio
"""

#-------------------------------------------------------------------------------

#import twilio
from twilio.rest import Client
import urllib2
import json



class Communication(object):
  def __init__(self):
    self.temp = ""
    self.location = ""
    self.weather = ""
    self.messageT = ""
    
  def get_weather(self, city, state):
    """This function gets weather from Weather Underground, modifies city strings with spaces, and prints the output.
    input: city and state
    outut: message
    """
    alt_city = ""
    if " " in city:
      print "yes"
      for c in city:
        if c == " ":
          alt_city += "_"
        else:
          alt_city += c
    else:
        print "no"
    
    url="http://api.wunderground.com/api/3b75aa5f752e5e79/conditions/q/%s/%s.json" % (state, alt_city)
  
    f = urllib2.urlopen(url)  # request the url from wunderground
    json_string = f.read()    # read the data returned into a string variable 
    # print 'json_string', json_string
  
    parsed_json = json.loads(json_string) # convert the string it to a json object
  
    #weather, temperature, and observation location
  
    self.temp = parsed_json['current_observation']['temp_f']
    self.location = parsed_json['current_observation']['observation_location']['full']
    self.weather = parsed_json['current_observation']['weather']
  
    self.messageT = "Temp in %s is %sF, Weather is %s. " % (city, self.temp, self.weather)
  
    f.close()
    print self.messageT
    
  def  create_message(self):
    """This function provides advice for people based on the weather.
    input: nothing
    output: modified messageT
    """
    if self.temp <= 40:
      self.messageT += "Wear warm clothes!"
    if self.weather == "Rain":
      self.messageT += "Wear a rain jacket."
    if self.weather == "Snow":
      self.messageT += "Wear snow boots."
      
  def send_sms(self, phone_num): #text_message): #, phone_num, text_message):
    """This function actually sends the message using Twilio.
    Input: phone number (and message)
    Output: sent message
    """
    # Your Account Sid and Authorization Token from twilio.com/user/account
    account_sid = "ACfffa98408f30b9451604fd261e0f7a82" # You must use your own sid
    auth_token  = "76a4ace8cf123fa51bd8fa5d2897a015"   # You must use your own token

    client = Client(account_sid, auth_token) # Create an client object
    
    #print self.messageT
    try:
       client.api.account.messages.create(
            body=self.messageT,       # Replace with a string containing your message
            to=phone_num,     # Replace with your verified destination phone number
            from_="+15622702170" # Replace with your Twilio number (562) 270-2170
            )
    except:
       print "There was an error sending your message"

    
if __name__ == "__main__":
  com = Communication()
  com.get_weather("New York", "NY")
  com.create_message()
  com.send_sms("+13472813976")

  