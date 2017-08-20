import os
import sys
import json

from test import lyric_print

from cred import *
import signal
import time

from savingdata import newuser, olduser_savingdata, olduser_or_newuser, search_song, user_song


import requests
from flask import Flask, request

import threading

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
	# when the endpoint is registered as a webhook, it must echo back
	# the 'hub.challenge' value it receives in the query arguments
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200

	return "Hello world", 200

#sets URL for controller
@app.route('/', methods=['POST'])
def webhook():
	# endpoint for processing incoming messaging events
	data = request.get_json()
	log(data)  # you may not want to log every incoming message in production, but it's good for testing

	if data["object"] == "page":
		for entry in data["entry"]:
			for messaging_event in entry["messaging"]:

				if messaging_event.get("message"):  # someone sent us a message
					sender_id = messaging_event["sender"]["id"]		# the facebook ID of the person sending you the message
					recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
					message_text = messaging_event["message"]["text"]  # the message's text
					#Possible_greeintgs entered from the user
					possible_greetings = ["Hello", "hello", "hi", "Hi", "yo", "Yo"]
					#Possible entries by the user
					possible_request_song = ["Bubbles, I would like to see the songs I requested before", "what songs have I requested before"]

					#run a check if he is a new user or old user
					if olduser_or_newuser(sender_id) == "new":
						newuser(sender_id)

					#Check whether the message can be found in the possible_greetings array
					#Check if the user is greeting the bot
					if message_text in possible_greetings:
						send_message(sender_id,"Hello, if you want to request lyrics to a song please follow this format (--> song name, artist name) or if you want to see the previous songs you requested just ask") 
					
					#Check whether the message sent can be found in the possible_request_song array
					#Check if the user wants to list the songs that it has requested before
					elif message_text in possible_request_song:
						send_message(sender_id, user_song(sender_id))
					else:
						#Error Catching, if people enter stuff that cannot be processed by methods
						#Examples of invalid inputs that do not fall under any method provided:
							#lajkdf 
							#280-234
					 	try:
							send_message(sender_id, lyric_print(message_text))

							olduser_savingdata(sender_id, message_text, lyric_print(message_text))
						except (TypeError, IndexError, RuntimeError,  UnicodeEncodeError, KeyError):
							send_message(sender_id, "Either you forgot the name of your song, or the artist name is wrong, or you just talking gibirish")
							break

				if messaging_event.get("delivery"):  # delivery confirmation
					pass
				if messaging_event.get("optin"):  # optin confirmation
					pass
				if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
					pass
	return "ok", 200
def send_message(recipient_id, message_text):

	log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
	#The format which the log is incoming

	params = { #dictionary
		"access_token": os.environ["PAGE_ACCESS_TOKEN"] #os.environ --> path name of "page_access_token", basically gets the PAGE_ACCESS_TOKEN that has been entered
	}

	headers = { #dictionary
		"Content-Type": "application/json" #
	}
	data = json.dumps({
		"recipient": {
			"id": recipient_id
		},
		"message": {
			"text": message_text
		}
	})
	r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
	if r.status_code != 200:
		log(r.status_code)
		log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
	print str(message)
	sys.stdout.flush()

#makes a get request to the webhook to make it stay awake
def stay_awake():
	r = requests.post('https://fierce-thicket-83098.herokuapp.com/', auth=('user', 'pass'))
	a = r.status_code
	return a

threading.Timer(1600, stay_awake)


if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port) #Use this only if u dont use gunicorn
	#app.run(debug=True)



