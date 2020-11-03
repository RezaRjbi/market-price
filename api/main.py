from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from scraper import MakeResponse, get_price

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address
)
@app.route('/')
@limiter.limit('6/minute',error_message='You reached the limit')
def price():
    ip = request.remote_addr
    price =MakeResponse(get_price())
    return jsonify({'items': price.price, 'time': price.time, 'ip': ip})

if __name__ == '__main__':
    app.run(debug=True)