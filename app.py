import json
from flask import Flask, render_template, request

from services.telegram.TelegramSTR import *
from services.telegram.TelegramTR2 import *
from services.telegram.TelegramBG88 import *
from services.telegram.TelegramTest import *
from services.telegram.TelegramGS import *
from services.telegram.TelegramGC import *

app = Flask(__name__)


@app.route('/send/test')
def delete_async():
    bot = TelegramTest().get_bot()
    from telegram.ext import Updater
    u = Updater(bot=bot, use_context=True)
    q = u.job_queue
    for i in range(10):
        TelegramTest().send_message('test' + str(i))
        print(i)
        # jq.run_once(TelegramTest().send_message('test'), 0.1)

    return 'qqq'


@app.route('/tag/daily/<project>')
def tag_daily(project):
    if project == 'gs':
        TelegramGS().tag()
    return project


@app.route('/read/<name>')
def read(name):
    docs = []
    if name == 'test':
        docs = TelegramTest().read()
    if name == 'bg88':
        docs = TelegramBG88().read()
    if name == 'tr2':
        docs = TelegramTR2().read()
    if name == 'gs':
        docs = TelegramGS().read()
    if name == 'gc':
        docs = TelegramGC().read()
    return render_template(
        'telegram/read.html',
        docs=docs
    )


@app.route('/write/<name>')
def write(name):
    if name == 'test':
        TelegramTest().write()
    if name == 'bg88':
        TelegramBG88().write()
    if name == 'tr2':
        TelegramTR2().write()
    if name == 'gs':
        TelegramGS().write()
    return 'OK'


@app.route('/delete/<name>')
def delete(name):
    if name == 'test':
        TelegramTest().delete()
    if name == 'bg88':
        TelegramBG88().delete()
    if name == 'tr2':
        TelegramTR2().delete()
    if name == 'gs':
        TelegramGS().delete()
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
    TelegramTest().listen_webhook(d)
    TelegramTR2().listen_webhook(d)
    TelegramSTR().listen_webhook(d)
    TelegramGS().listen_webhook(d)
    TelegramGC().listen_webhook(d)
    return 'OK'


@app.route('/voice/<text>')
def index(text):
    TelegramTest().send_tts_audio(text)
    return 'OK'


@app.route('/home')
def home():
    return render_template(
        'home.html',
        config=get_config(),
        groups=['gs', 'test', 'tr2', 'bg88']
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
