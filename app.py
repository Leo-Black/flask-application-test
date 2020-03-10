'''
Leo Black
Flask Application Test
Created 17/02/20
'''

from sqlite3 import connect # Gives the ability to connect to sqlite3 databases
from flask import Flask, g, redirect, render_template, request # Allows the use of Flask, g, redirecting, HTML templates and requesting

app = Flask(__name__) # Initialises the app

def get_database():
    '''Connects to the database 'database.db' using getattr and returns the connection. If the database is not found, it connects manually.'''
    database_connection = getattr(g, '_database', None)
    if not bool(database_connection):
        database_connection = g._database = connect('database.db')
    return database_connection

@app.route('/')
def home():
    '''Renders the HTML template 'home.html' as the home page.'''
    return render_template('home.html')

@app.route('/index', methods=['GET', 'POST',])
def index():
    '''Renders the HTML template 'index.html' and sets array to range(1, 101).'''
    return render_template('index.html', array=range(1, 101))

@app.route('/data')
def data():
    '''Renders the HTML template 'data.html', sets result to the items in test_table and sets length to len(result).'''
    cursor = get_database().cursor()
    sql_query = 'SELECT * FROM test_table' # Creates an SQL statement that finds all items in test_table
    cursor.execute(sql_query)
    result = cursor.fetchall()
    return render_template('data.html', result=result, length=len(result)) # Renders the data.html template and sets the default values for result and length

@app.route('/add', methods=["GET", "POST"])
def add():
    '''Adds inputted item to the database, redirects to 'data.html' and commits the changes.'''
    if request.method == 'POST':
        cursor = get_database().cursor()
        new_name = request.form['item_name']
        sql_query = 'INSERT INTO test_table(name) VALUES (?)' # Creates an SQL statement that adds the requested item into the table
        cursor.execute(sql_query, (new_name,))
        get_database().commit() # Commits the executed SQL statement
    return redirect('/data') # Redirects back to the /data page

@app.route('/delete', methods=["GET", "POST"])
def delete():
    '''Deletes inputted item from the database, redirects to 'data/html' and commits the changes.'''
    if request.method == 'POST':
        cursor = get_database().cursor()
        id = int(request.form['item_name'])
        sql_query = 'DELETE FROM test_table WHERE id=?' # Creates an SQL statement that deletes the requested item from the table
        cursor.execute(sql_query, (id,))
        get_database().commit() # Commits the executed statement
    return redirect('/data') # Redirects back to the /data page

@app.teardown_appcontext
def close_connection(exception):
    '''Checks if there is a connection to the database and closes it.'''
    database_connection = getattr(g, '_database', None)
    if bool(database_connection):
        database_connection.close()
    return

if __name__ == '__main__':
    app.run(debug=True)