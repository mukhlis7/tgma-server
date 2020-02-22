from psycopg2.extras import DictCursor
import psycopg2
from flask import g


def connect_db():
	conn = psycopg2.connect('postgres://odfyojhhgclbub:7fadf9298c8d0678544bd870ca26438db58f22c9ccb239cb5b22a3327c6a0e2d@ec2-34-200-116-132.compute-1.amazonaws.com:5432/ddle3pd8i04opt', cursor_factory=DictCursor)
	conn.autocommit = True
	sql = conn.cursor()

	return conn, sql


def get_db():
	
	db = connect_db()

	if not hasattr(g,'postgres_db_conn'):
		g.postgres_db_conn = db[0]

	if not hasattr(g, 'postgres_db_cur'):
		g.postgres_db_cur = db[1]

	return g.postgres_db_cur


def init_db():

	db = connect_db()

	db[1].execute(open('schema.sql', 'r').read())
	db[1].close()
	db[0].close()

