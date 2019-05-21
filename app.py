import json
from flask import Flask, render_template, request

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


@app.route('/read/bg88')
def read_bg88():
    docs = TelegramBG88().read()
    return render_template(
        'telegram/read.html',
        docs=docs
    )


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
    return render_template(
        'index.html',
        config=get_config()
    )


@app.template_filter('ts_to_date')
def ts_to_date(ts):
    from datetime import datetime
    import pytz
    utc_moment_naive = datetime.utcfromtimestamp(ts)
    utc_moment = utc_moment_naive.replace(tzinfo=pytz.utc)
    return utc_moment.astimezone(pytz.timezone('Asia/Taipei')).strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    app.run()
