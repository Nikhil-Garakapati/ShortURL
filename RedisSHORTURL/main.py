from flask import Flask , render_template , request , redirect
import base64,math
import redis
import string
import urlparse
import werkzeug.exceptions

app=Flask(__name__)
redis=redis.Redis()
#r = redis.StrictRedis(host='localhost', port=6379, db=0)

def base62con(num):
    
    '''Using Base62 enconding as it gives 3.5 trillion combinations'''
    
    base = string.digits + string.lowercase + string.uppercase
    hashed_string = ''
    while num > 0:
        hashed_string = base[num % 62] + hashed_string
        num = num/62
    return hashed_string


@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/shortified', methods=['POST'])
def return_shortened():
    url_to_parse = request.form['input-url']
    parts = urlparse.urlparse(url_to_parse)
    if not parts.scheme in ('http', 'https'):
        error = "Please enter valid url"
    else:
        short_id = shortified(url_to_parse)
    return render_template('result.html', short_id=short_id)


@app.route("/<short_id>")
def expand_to_long_url(short_id):
    link_target = redis.get('url-target:' + short_id)
    if link_target is None:
        raise NotFound()
    return redirect(link_target)
    
    
def shortified(url):
        short_id = redis.get('reverse-url:' + url)
        if short_id is not None:
            return short_id
        url_num = redis.incr('last-url-id')
        short_id = b62_encode(url_num)
        redis.set('url-target:' + short_id, url)
        redis.set('reverse-url:' + url, short_id)
        return short_id

if __name__ == '__main__':
    app.run(debug=True)

