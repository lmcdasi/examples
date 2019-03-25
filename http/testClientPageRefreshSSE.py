#!/usr/bin/python3

# Client refreshes http page via Server Event Source (SSE)

import datetime
import random
from http.server import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 8181

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
        #Handles "/"
	def do_main(self):
		self.send_response(200)
		self.send_header('Content-type','text/html; charset=utf-8')
		self.end_headers()

		sse_test_page = """
<!DOCTYPE html>
   <html>
      <body>
         <h1>Getting server updates</h1>
            <div id="result"></div>
            <script>
               if (typeof(EventSource) !== "undefined") {
                  var source = new EventSource("event");
                  source.onmessage = function(event) {
                     document.getElementById("result").innerHTML += event.data + "<br>";
                     console.log(event.data);
                  };
                  //source.onerror = function(error) {
                  //   console.log("EventSource failed - type: " + error.type);
                  //}
               } else {
                  document.getElementById("result").innerHTML = "Sorry, your browser does not support server-sent events...";
               }

            </script>
      </body>
   </html>
		"""

		self.wfile.write(bytes(sse_test_page, "utf-8"))

		return

	#Handles "/event"
	def do_event(self):
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
	
	#Handler for the GET requests
	def do_GET(self):
		self.protocol_version="HTTP/1.1"
		if self.path == '/':
			self.do_main()
		elif self.path == '/event':
			self.do_event()

		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print ('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print('^C received, shutting down the web server')
	server.socket.close()
