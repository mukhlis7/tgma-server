#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, g, request, jsonify, url_for, request, session
from database import get_db
import string
import random

app = Flask(__name__)


def close_db(error):
	if hasattr(g,'postgres_db_conn'):
		g.postgres_db_conn.close()

	if hasattr(g,'postgres_db_cur'):
		g.postgres_db_cur.close()



def username_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def password_generator(size=18, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))



@app.route('/register', methods=['GET', 'POST'])
def register_user():
	db = get_db()

	fullname = input("[+]  Enter a Fullname: ")
	username = username_generator()
	password = password_generator()

	print("Fullname : " + fullname)
	print("Username : " + username)
	print("Password : " + password)

	db.execute('select id from tgmauser where username = %s', (username, ))
	existing_user_username = db.fetchone()

	if existing_user_username:
		print('Failed to Register! Username already Exist')
		return('Failed to Register! Username already Exist')

	db.execute('insert into tgmauser (fullname, username, password, verified) values (%s, %s, %s, %s)', (fullname, username, password, '1'))
	print("Registered!")
	return("Registered!")


@app.route('/allusers', methods=['GET', 'POST'])
def fetch_all_users():

	db = get_db()
	db.execute('select * from tgmauser', )
	all_users = db.fetchall()
	length = len(all_users)
	for i in range(length):
		print("\n" + str(all_users[i]) + "\n")

	#print(all_users)

	return jsonify({'result':'True'})


if __name__ == '__main__':

	#sio.run(app, host="0.0.0.0", port=80, debug=True)
	app.run(host="0.0.0.0", port=80, debug=True)
