from app import app
from flask import Flask, render_template, request
from collections import namedtuple
from google import search
from alchemyapi import AlchemyAPI
from encodings import hex_codec
from encodings import ascii
import httplib,urllib2
import json
import sys

api_key = "83da2d0deaef076648b28972905d2f8c1f5e3c0f"
words = []

def keywords(myURL):
	url = "http://access.alchemyapi.com/calls/url/URLGetRankedKeywords?apikey=%s&url=%s&outputMode=json" % (api_key,myURL)

	json = urllib2.urlopen(url).read()

	the_data = eval(json)

	for keyword in range(0,4):
		words.append(the_data['keywords'][keyword]['text'])

	return words
	

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/search', methods=['GET', 'POST'])
def contact():
	if request.method == 'POST':
		urlink = request.form.get('url', '')
	else:
		urlink = request.args.get('url', '')

	try:
		f = urllib2.urlopen(urllib2.Request(urlink))
		deadLinkFound = False
	except:
		deadLinkFound = True

	if(deadLinkFound == True):  
		return render_template('error.html', error = "Please check your inputs, it is crucial that you enter a proper URL.")

	newkeys = keywords(urlink)
	templinks = []
	for key in range(len(newkeys)):
		for url in search(str(newkeys[key]), stop = 5):
			templinks.append(url)
			break
				

	return render_template('linkspage.html', thelink1 = str(templinks[0]), thelink2 = str(templinks[1]), thelink3 = str(templinks[2]), thelink4 = str(templinks[3]))
	#return render_template('linkspage.html', thelink1 = str(newkeys[0]), thelink2 = str(newkeys[1]), thelink3 = str(newkeys[2]), thelink4 = str(newkeys[2]))