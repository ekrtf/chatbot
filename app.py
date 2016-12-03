import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def main_route():
	return 'Hello'

@app.route('/webhook', methods=['POST'])
def receive_message():
	return 'Do something with message'

if __name__=='__main__':
	app.run(host='localhost', port=8080)
