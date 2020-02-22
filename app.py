#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, g, request, jsonify, url_for, request, session
from database import get_db
import time
import datetime
from functools import wraps
import jwt

app_passwd = 'mysecretMg7Mukhlis7HelloFromThisWorld!'

app = Flask(__name__)

app.config['SECRET_KEY'] = app_passwd

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']

		if not token:
			loggedin = False
			return jsonify({'loggedin':loggedin,'message' : 'Token is missing!'})

		try:
			data = jwt.decode(token, app_passwd)
			db = get_db()
			db.execute('select username, verified from tgmauser where username = %s', (data['username'], ))
			data_user = db.fetchone()
			print(data_user)
			current_user = data_user[0]
			verified = data_user[1]
			print(verified)
			loggedin = True
			#current_user = User.query.filter_by(public_id=data['public_id']).first()
		except:
			loggedin = False
			return jsonify({'loggedin':loggedin,'message' : 'Token is invalid!'})

		return f(current_user, verified, *args, **kwargs)

	return decorated



@app.route('/')
def index():
	"""Serve the client-side application."""
	return "Server ROOT DIR"


def close_db(error):
	if hasattr(g,'postgres_db_conn'):
		g.postgres_db_conn.close()

	if hasattr(g,'postgres_db_cur'):
		g.postgres_db_cur.close()


@app.route('/logintoken', methods=['POST'])
@token_required
def logintoken(current_user,verified):

	if request.method == 'POST':
		loggedin = True
		print(verified)
		print(current_user)
		message = "loggedin!"
		return jsonify({'loggedin':loggedin, 'message':message, 'authorized':verified})



@app.route('/login', methods=['POST'])
def login():

	if request.method == 'POST':
		db = get_db()
		data = request.get_json()
		username = data["username"]
		password = data["password"]

		print("Data From User: " + username + " "+ password)

		db.execute('select * from tgmauser where username = %s', (username, ))
		user_result = db.fetchone()

		print("Data From database with username: " + str(user_result))

		if user_result == None:

			error = 'The username is incorrect'
			loggedin = False
			#print("Data From database: " + str(user_result))

		else:

			if user_result['password'] == password:
				loggedin = True
				verified = user_result['verified']
				token = jwt.encode({'username' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=44640)}, app_passwd)
				return jsonify({'loggedin':loggedin, 'message':'You are logged In!', 'token':token.decode('UTF-8'), 'authorized':verified})

			else:
				loggedin = False
			error = 'The password is incorrect.'


		return jsonify({'loggedin':loggedin, 'message':error})





if __name__ == '__main__':

	#sio.run(app, host="0.0.0.0", port=80, debug=True)
	app.run(host="0.0.0.0", port=8080, debug=True)

	#app.run()
	# wrap Flask application with engineio's middleware
   # app = socketio.Middleware(sio, app)

	# deploy as an eventlet WSGI server
	#eventlet.wsgi.server(eventlet.listen(('', 8000)), app)