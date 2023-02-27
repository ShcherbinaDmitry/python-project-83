import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_db():
    print('DATABASE URL:')
    print(DATABASE_URL)
    return psycopg2.connect(DATABASE_URL)


def get_urls():
    conn = get_db()
    curs = conn.cursor(cursor_factory=NamedTupleCursor)

    curs.execute('SELECT * FROM urls ORDER BY id DESC;')
    urls = curs.fetchall()

    curs.close()
    conn.close()
    return urls


def get_url_by_id(id):
    conn = get_db()
    curs = conn.cursor(cursor_factory=NamedTupleCursor)

    curs.execute('SELECT * FROM urls WHERE id = %s;', (id,))
    url = curs.fetchone()

    curs.close()
    conn.close()
    return url


def get_url_by_name(name):
    conn = get_db()
    curs = conn.cursor(cursor_factory=NamedTupleCursor)

    curs.execute('SELECT * FROM urls WHERE name = %s;', (name,))
    url = curs.fetchone()

    curs.close()
    conn.close()

    return url


def add_url(url):
    conn = get_db()
    curs = conn.cursor(cursor_factory=NamedTupleCursor)

    curs.execute(
        'INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;',
        (url, datetime.now())
    )
    id = curs.fetchone().id

    conn.commit()

    curs.close()
    conn.close()

    return id


def get_checks():
    conn = get_db()
    curs = conn.cursor(cursor_factory=NamedTupleCursor)

    curs.execute(
        'SELECT DISTINCT ON (url_id) * FROM url_checks ORDER BY url_id DESC'
    )
    checks = curs.fetchall()

    curs.close()
    conn.close()

    return checks


def get_checks_for_url(id):
    conn = get_db()
    curs = conn.cursor(cursor_factory=NamedTupleCursor)

    curs.execute('SELECT * FROM url_checks WHERE url_id = %s', (id, ))
    checks = curs.fetchall()

    curs.close()
    conn.close()

    return checks


def add_check(data):
    conn = get_db()
    curs = conn.cursor(cursor_factory=NamedTupleCursor)

    curs.execute(
        'INSERT INTO url_checks\
        (url_id, status_code, h1, title, description, created_at)\
         VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;',
        (
            data['url_id'],
            data['status_code'],
            data['h1'], data['title'],
            data['description'],
            datetime.now()
        )
    )
    id = curs.fetchone().id

    conn.commit()

    curs.close()
    conn.close()

    return id
