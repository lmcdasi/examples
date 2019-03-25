#!/usr/bin/python3

import asyncio
import datetime
import random
import threading
import websockets
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT_NUMBER = 8181
WEBSOCK_POR_NUMBER=8182

#This class will handles any incoming request from
#the browser 
async def websend(websocket, path):
	while True:
		now = datetime.datetime.utcnow().isoformat() + 'Z'
		await websocket.send(now)
		await asyncio.sleep(random.random() * 3)

def worker():
	asyncio.set_event_loop(asyncio.new_event_loop())

	start_server = websockets.serve(websend, '127.0.0.1', WEBSOCK_POR_NUMBER)

	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()

class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()

		# Send the html message
		self.wfile.write(bytes("<!DOCTYPE html>\n", "utf-8"))
		self.wfile.write(bytes("<html>\n", "utf-8"))
		self.wfile.write(bytes("<head>\n", "utf-8"))
		self.wfile.write(bytes("\t<title>WebSocket demo</title>\n", "utf-8"))
		self.wfile.write(bytes("</head>\n", "utf-8"))
		self.wfile.write(bytes("<body>\n", "utf-8"))
		self.wfile.write(bytes("\t<h1>Getting server updates</h1>\n", "utf-8"))
		self.wfile.write(bytes("\t<script>\n", "utf-8"))
		self.wfile.write(bytes('\t\tvar ws = new WebSocket("ws://127.0.0.1:' + str(WEBSOCK_POR_NUMBER) + '/"),\n', "utf-8"))
		self.wfile.write(bytes("\t\tmessages = document.createElement('ul');\n", "utf-8"))
		self.wfile.write(bytes("\t\tws.onmessage = function (event) {\n", "utf-8"))
		self.wfile.write(bytes("\t\t\tvar messages = document.getElementsByTagName('ul')[0];\n", "utf-8"))
		self.wfile.write(bytes("\t\t\tmessage = document.createElement('li');\n", "utf-8"))
		self.wfile.write(bytes("\t\t\tcontent = document.createTextNode(event.data);\n", "utf-8"))
		self.wfile.write(bytes("\t\t\tmessage.appendChild(content);\n", "utf-8"))
		self.wfile.write(bytes("\t\t\tmessages.appendChild(message);\n", "utf-8"))
		self.wfile.write(bytes("\t\t};\n", "utf-8"))
		self.wfile.write(bytes("\t\tdocument.body.appendChild(messages);\n", "utf-8"))
		self.wfile.write(bytes("\t</script>\n", "utf-8"))
		self.wfile.write(bytes("</body>\n", "utf-8"))
		self.wfile.write(bytes("</html>", "utf-8"))

		return

try:
	#Create a websocket
	t = threading.Thread(target=worker)
	t.start()

	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()
