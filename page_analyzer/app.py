from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def get_urls():
    sites = [{
        'id': 1,
        'name': 'Test site',
        'last_check': '2023-01-29',
        'response_code': 200
    }]
    return render_template('urls/index.html', sites=sites)