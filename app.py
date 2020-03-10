import sqlite3
from flask import Flask, g, redirect, render_template, request

app = Flask(__name__)
database = 'database.db'

def get_database():
    database_connection = getattr(g, '_database', None)
    if not bool(database_connection):
        database_connection = g._database = sqlite3.connect(database)
    return database_connection

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index', methods=['GET', 'POST',])
def index():
    return render_template('index.html', array=range(1,101))

@app.route('/data')
def data():
    cursor = get_database().cursor()
    sql_query = 'SELECT * FROM test_table'
    cursor.execute(sql_query)
    result = cursor.fetchall()
    return render_template('data.html', result=result, length=len(result))

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        cursor = get_database().cursor()
        new_name = request.form['item_name']
        sql_query = 'INSERT INTO test_table(name) VALUES (?)'
        cursor.execute(sql_query, (new_name,))
        get_database().commit()
    return redirect('/data')

@app.route('/delete', methods=["GET", "POST"])
def delete():
    if request.method == 'POST':
        cursor = get_database().cursor()
        id = int(request.form['item_name'])
        sql_query = 'DELETE FROM test_table WHERE id=?'
        cursor.execute(sql_query, (id,))
        get_database().commit()
    return redirect('/data')

@app.teardown_appcontext
def close_connection(exception):
    database_connection = getattr(g, '_database', None)
    if bool(database_connection):
        database_connection.close()
    return

if __name__ == '__main__':
    app.run(debug=True)
