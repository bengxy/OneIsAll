from flask import Flask, render_template, request, session, g,\
    redirect, url_for, abort, flash
from flaskext.mysql import MySQL
import time

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'Adatabase'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

@app.route('/api/<date>')
def oneisall(date):
    #check date format
    if not is_valid_date(date):
        return render_template('404.html')
    
    return date

@app.route('/mysql')
def check():
    username = 'root'
    password = '123'
    cursor = mysql.connect().cursor()
    cursor.execute("select * from Atable")
    data = cursor.fetchone()

    if data:
        return str(data)
    else:
        return 'BadCase'



def get_db():
    if not hasattr(g, 'mysql'):
        g.mysql = connect_db()
    return g.mysql

def close_db(error):
    if hasattr(g, 'mysql'):
        g.mysql.close()
          
def is_valid_date(str):
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False

if __name__ == '__main__':
    app.run(debug=True)