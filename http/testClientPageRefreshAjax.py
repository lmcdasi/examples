#!/usr/bin/python3

# Client refreshes page via AJAX or XMLHTTPRequest. If server goes down the page
# continues to send requests and when sever comes back the page continues to refresh
# the page

import datetime
import random
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT_NUMBER = 8181

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for 1st GET request
	def do_main(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()

		# Send the client AJAX page
		self.wfile.write(bytes("<!DOCTYPE html>\n", "utf-8"))
		self.wfile.write(bytes("<html>\n", "utf-8"))
		self.wfile.write(bytes("<head>\n", "utf-8"))
		self.wfile.write(bytes("\t<title>AJAX demo</title>\n", "utf-8"))
		self.wfile.write(bytes("\t<h1>Getting server updates</h1>\n", "utf-8"))
		self.wfile.write(bytes('\t<script type="text/javascript">\n', "utf-8"))
		self.wfile.write(bytes('\t\tfunction loadXMLDoc() {\n', "utf-8"))
		self.wfile.write(bytes('\t\t\tvar xmlhttp;\n', "utf-8"))
		self.wfile.write(bytes('\t\t\tif (window.XMLHttpRequest) {\n', "utf-8"))
		self.wfile.write(bytes('\t\t\t\txmlhttp = new XMLHttpRequest();\n', "utf-8"))
		self.wfile.write(bytes('\t\t\t} else {// code for IE6, IE5\n', "utf-8"))
		self.wfile.write(bytes('\t\t\t\txmlhttp = new ActiveXObject("Microsoft.XMLHTTP");\n', "utf-8"))
		self.wfile.write(bytes('\t\t\t}\n', "utf-8"))
		self.wfile.write(bytes('\t\t\txmlhttp.onreadystatechange = function () {\n', "utf-8"))
		self.wfile.write(bytes('\t\t\t\tif (xmlhttp.readyState == 4 && xmlhttp.status == 200) {\n', "utf-8"))
		self.wfile.write(bytes('\t\t\t\t\tdocument.getElementById("myDiv").innerHTML = xmlhttp.responseText;\n', "utf-8"))
		self.wfile.write(bytes('\t\t\t\t}\n', "utf-8"))
		self.wfile.write(bytes('\t\t\t}\n', "utf-8"))
		self.wfile.write(bytes('\t\t\txmlhttp.open("GET", "/ajax", true);\n', "utf-8"))
		self.wfile.write(bytes('\t\t\txmlhttp.send();\n', "utf-8"))
		self.wfile.write(bytes('\t\t}\n', "utf-8"))
		self.wfile.write(bytes('\t\tsetInterval(loadXMLDoc, 2000);', "utf-8"))
		self.wfile.write(bytes('\t</script>\n', "utf-8"))
		self.wfile.write(bytes("</head>\n", "utf-8"))
		self.wfile.write(bytes("<body>\n", "utf-8"))
		self.wfile.write(bytes('\t<div id="myDiv"></div>', "utf-8"))
		self.wfile.write(bytes("</body>\n", "utf-8"))
		self.wfile.write(bytes("</html>", "utf-8"))

		return

	def do_ajax(self):
		now =  datetime.datetime.utcnow().strftime("%c")
		now = "data: " + str(now) + "\n\n";

		self.send_response(200)
		self.send_header('Cache-Control', 'no-cache')
		self.send_header('Connection', 'keep-alive')
		self.send_header('Content-Length', len(now))
		self.send_header('Content-type', 'text/event-stream')
		self.end_headers()

		self.wfile.write(bytes(now, "utf-8"))

		return

	def do_GET(self):
		self.protocol_version="HTTP/1.1"
		if self.path == '/':
			self.do_main()
		elif self.path == '/ajax':
			self.do_ajax()

		return


try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print('^C received, shutting down the web server')
	server.socket.close()
