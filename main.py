from flask import Flask, request
import datetime
import pymysql
import os
from dotenv import load_dotenv
import json

app = Flask(__name__)
load_dotenv(verbose=True)

def db_connection():
    return pymysql.connect(
        user = 'admin',
        passwd=os.getenv('db_pw'),
        host=os.getenv('db_url'),
        port=3306,
        db='desk',
        charset='utf8'
    )

def handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

@app.route('/')
def health_check():
    return 'OK'

@app.route('/test', methods=['POST'])
def test():
    if request.method == 'POST':
        form = request.form
        print(form['id'])
        return form

@app.route('/upsert', methods=['POST'])
def upsert():
    db = db_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        form = request.form
    elapsed = form['elapsed']
    query = f'INSERT INTO track (user, elapsed, date, start) VALUES ("Loveliest", "{elapsed}", "{today}", "{now}") ON DUPLICATE KEY UPDATE elapsed="{elapsed}", end="{now}"'
    print(query)
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()

@app.route('/insertimage', methods=['POST'])
def insertimage():
    db = db_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        form = request.form
    uri = form['uri']
    query = f'INSERT INTO image (user, date, uri) VALUES ("Loveliest", "{now}", "{uri}")'
    print(query)
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()

@app.route('/select', methods=['POST'])
def select():
    db = db_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    today = datetime.datetime.now().strftime('%Y-%m-%d')

    query = f'SELECT * FROM track WHERE date = "{today}"'
    print(query)
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)
    db.close()
    return json.dumps(result, default=handler)

@app.route('/selectimage', methods=['POST'])
def selectimage():
    db = db_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start = 'SUBTIME( NOW(), TIMEDIFF( NOW(), CAST(DATE(NOW()) AS DATETIME) ) )'

    query = f'SELECT * FROM image WHERE date > {start} AND date <= "{now}"'
    print(query)
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return json.dumps(result, default=handler)

@app.route('/selectVideo', methods=['POST'])
def selectVideo():
    db = db_connection()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    now = datetime.datetime.now().strftime('%Y-%m-%d')

    query = f'SELECT * FROM video WHERE date = "{now}"'
    print(query)
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return json.dumps(result, default=handler)

