from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages, request, abort
import os
import requests
from page_analyzer.validator import validate, normalize
import page_analyzer.db as db
from itertools import zip_longest
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config.update(
    SECRET_KEY = os.getenv('SECRET_KEY')
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def urls():
    messages = get_flashed_messages(with_categories=True)
    sites = db.get_urls()
    checks = db.get_checks()
    sites_with_checks = zip_longest(sites, checks)

    return render_template('urls/index.html', sites=sites_with_checks, messages=messages)


@app.post('/urls')
def post_url():
    form_data = request.form.to_dict()
    url = normalize(form_data.get('url'))
    errors = validate(url)

    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('index.html', url_name=url), 422

    ## Запись в бд
    existing_url = db.get_url_by_name(url)

    if not existing_url:
        id = db.add_url(url)
        flash('Страница успешно добавлена', 'success')
    else:
        flash('Страница уже существует', 'info')
        id = existing_url.id


    return redirect(url_for('show_url', id=id))

@app.get('/urls/<int:id>')
def show_url(id):
    messages = get_flashed_messages(with_categories=True)
    url = db.get_url_by_id(id)

    if not url:
        abort(404)
    checks = db.get_checks_for_url(id)
    return render_template('urls/show.html', url=url, checks=checks, messages=messages)


@app.post('/urls/<int:id>/checks')
def check_url(id):
    url = db.get_url_by_id(id).name

    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.RequstException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url', id=id))

    # Write check to db
    page = res.text
    page_data = {'url_id': id, 'status_code': res.status_code, **get_data(page)}
    db.add_check(page_data)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('show_url', id=id))


def get_data(page):
    contents = BeautifulSoup(page, 'html.parser')
    title = contents.find('title').text if contents.find('title') else ''
    h1 = contents.find('h1').text if contents.find('h1') else ''
    description = contents.find('meta', attrs={'name': 'description'})
    if description:
        description = description['content']
    else:
        description = ''
    return {
        'title': title[:255],
        'h1': h1[:255],
        'description': description[:255],
    }

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500