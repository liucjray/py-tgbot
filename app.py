from flask import Flask
from flask import request
import json

from services.TelegramTR2 import *
from services.TelegramBG88 import *
from services.TelegramTest import *

app = Flask(__name__)


@app.route('/write/tr2')
def write_tr2():
    TelegramTR2().write()
    return 'OK'


@app.route('/delete/tr2')
def delete_tr2():
    TelegramTR2().delete()
    return 'OK'


@app.route('/write/bg88')
def write_bg88():
    TelegramBG88().write()
    return 'OK'


@app.route('/delete/bg88')
def delete_bg88():
    TelegramBG88().delete()
    return 'OK'


@app.route('/write/test')
def write_test():
    TelegramTest().write()
    return 'OK'


@app.route('/delete/test')
def delete_test():
    TelegramTest().delete()
    return 'OK'


@app.route('/set_webhook')
def set_webhook():
    msg = TelegramBG88().set_webhook()
    return msg


@app.route('/listen_webhook', methods=['POST'])
def listen_webhook():
    # json = request.get_json(force=True)
    d = json.loads(s=request.data)
    TelegramBG88().listen_webhook(d)
    return 'OK'


@app.route('/')
def index():
    config = get_config()
    links = [
        '<a target="_blank" href="' + config['TG']['UPDATE_URL'] + '">tgbot getUpdates</a>',
        '<a target="_blank" href="/set_webhook">/set_webhook</a>',
        '<hr>',
        '<a target="_blank" href="/write/tr2">/write/tr2</a>',
        '<a target="_blank" href="/delete/tr2">/delete/tr2</a>',
        '<hr>',
        '<a target="_blank" href="/write/bg88">/write/bg88</a>',
        '<a target="_blank" href="/delete/bg88">/delete/bg88</a>',
        '<hr>',
        '<a target="_blank" href="/write/test">/write/test</a>',
        '<a target="_blank" href="/delete/test">/delete/test</a>',
    ]
    html = ''
    for link in links:
        html += link + '<br>'
    return html


if __name__ == '__main__':
    app.run()
