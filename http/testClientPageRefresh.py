#!/usr/bin/python

# Clien refreshes full page at each interval of 3 sec

import time
import random
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 8181

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()

		# Send the html message
		self.wfile.write("<html><head><meta http-equiv=\"refresh\" content=\"3\"></head><body><h1>Hello World" + str(random.randrange(10)) + "</h1></body></html>")

		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()