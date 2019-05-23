from flask import Flask , render_template , request , redirect
import sqlite3
import math
import base64
from sqlite3 import OperationalError

app=Flask(__name__)
host='http://localhost:8080'

#Create an sqlite table 
conn = sqlite3.connect('A:\database.db')
print "Opened database successfully";


#Use executescript method to drop the table because it issues COMMIT before running the script
conn.executescript('''DROP TABLE IF EXISTS SHORT_URL''')
conn.execute('''
         CREATE TABLE SHORT_URL
         (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
         URL          TEXT    NOT NULL
         );''')
print "Table created successfully";


def base62con(num):
    
    '''Using Base62 enconding as it gives 3.5 trillion combinations'''
    
    base = string.digits + string.lowercase + string.uppercase
    hashed_string = ''
    while num > 0:
        hashed_string = base[num % 62] + hashed_string
        num = num/62
    return hashed_string


#print(base62(23232344))

def base10con(num):
    
    base = string.digits + string.lowercase + string.uppercase
    limit = len(num)
    dec = 0
    for i in xrange(limit):
        dec = 62 * dec + base.find(num[i])
    return dec


@app.route('/', methods=['GET', 'POST'])

def home():
    if request.method == 'POST':
        original_url = str_encode(request.form.get('url'))
        if urlparse(original_url).scheme == '':
            url = 'http://' + original_url
        else:
            url = original_url
        with sqlite3.connect('A:\database.db') as conn:
            cursor = conn.cursor()
            res = cursor.execute(
                'INSERT INTO SHORT_URL (URL) VALUES (?)',
                [base64.urlsafe_b64encode(url)]
            )
            encoded_string = base62con(res.lastrowid)
        return render_template('test.html', short_url=host + encoded_string)
    return render_template('test.html')


@app.route('/<short_url>')
def redirect_short_url(short_url):
    decoded = base10con(short_url)
    url = host  
    with sqlite3.connect('A:\database.db') as conn:
        cursor = conn.cursor()
        res = cursor.execute('SELECT URL FROM SHORT_URL WHERE ID=?', [decoded])
        try:
            short = res.fetchone()
            if short is not None:
                url = base64.urlsafe_b64decode(short[0])
        except Exception as e:
            print(e)
    return redirect(url)


if __name__ == '__main__':
    app.run(debug=True,host='localhost',port=8080)