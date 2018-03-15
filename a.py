from flask import Flask, render_template
#from flask import request, session, g
#from flask import redirect, url_for, abort, flash
from flaskext.mysql import MySQL
import time
import urllib2
import json

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'oneisall'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

@app.route('/api/<date>')
def oneisall(date):
    #check date format
    if not is_valid_date(date):
        return render_template('404.html')
    # check if exist in table
    con = mysql.connect()
    cursor = con.cursor()
    query = "select * from T where date = '{date}'".format(date=date)
    print(query)
    cursor.execute(query)
    data = cursor.fetchone()
    response = {}
    if data: # if exists, fetch from mysql
        print('exists')
        response['date'] = str(data[0])
        response['forward'] = data[1]
        response['words_info'] = data[2]
        response['img_url'] = data[3]
        response['pic_info'] = data[4]    
    else: # else get by url && save to mysql
        url = 'http://v3.wufazhuce.com:8000/api/channel/one/+'+date+'/%E6%9D%AD%E5%B7%9E%E5%B8%82'
        j = json.loads( urllib2.urlopen(url).read() )
        response['date'] = j['data']['date'].split(' ')[0]
        response['forward'] = j['data']['content_list'][0]['forward']
        response['words_info'] = j['data']['content_list'][0]['words_info']
        response['img_url'] = j['data']['content_list'][0]['img_url']
        response['pic_info'] = j['data']['content_list'][0]['pic_info']
        for k in response:
            response[k] = response[k].encode('UTF-8')
        query = "insert into T (`date`, `forward`, `words_info`, `img_url`, `pic_info`)\
                    values ('{date}','{forward}','{words_info}','{img_url}','{pic_info}')"\
                    .format(
                        date = response['date'],
                        forward = response['forward'],
                        words_info = response['words_info'],
                        img_url = response['img_url'],
                        pic_info = response['pic_info']
                    )
        print('execute')
        print(query)
        cursor.execute(query)
        con.commit()
    return json.dumps(response)

# @app.route('/mysql')
# def check():
#     username = 'root'
#     password = '123'
#     cursor = mysql.connect().cursor()
#     cursor.execute("select * from T")
#     data = cursor.fetchone()

#     if data:
#         return str(data)
#     else:
#         return 'BadCase'
          
def is_valid_date(s):
    try:
        t =  time.strptime(s, "%Y-%m-%d")
        base = time.strptime('2012-10-07', "%Y-%m-%d")
        if t<base:
            return False
        return True
    except:
        return False

if __name__ == '__main__':
    app.run(debug=True)