from flask import Flask
from services.TelegramTR2 import *
from services.TelegramBG88 import *

app = Flask(__name__)


@app.route('/write/tr2')
def write_tr2():
    tr2 = TelegramTR2()
    tr2.write()
    return 'OK'


@app.route('/delete/tr2')
def delete_tr2():
    tr2 = TelegramTR2()
    tr2.delete()
    return 'OK'


@app.route('/write/bg88')
def write_bg88():
    bg88 = TelegramBG88()
    bg88.write()
    return 'OK'


@app.route('/delete/bg88')
def delete_bg88():
    bg88 = TelegramBG88()
    bg88.delete()
    return 'OK'


@app.route('/')
def index():
    links = [
        '<a target="_blank" href="/write/tr2">write tr2</a>',
        '<a target="_blank" href="/delete/tr2">delete tr2</a>',
        '<a target="_blank" href="/write/bg88">write bg88</a>',
        '<a target="_blank" href="/delete/bg88">delete bg88</a>',
        '<a target="_blank" href="/write/test">write test</a>',
        '<a target="_blank" href="/delete/test">delete test</a>',
    ]
    html = ''
    for link in links:
        html += link + '<br>'
    return html


if __name__ == '__main__':
    app.run()
