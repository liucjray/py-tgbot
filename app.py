from flask import Flask, render_template, request

from services.telegram.TelegramSTR import *
from services.telegram.TelegramTR2 import *
from services.telegram.TelegramBG88 import *
from services.telegram.TelegramTest import *
from services.telegram.TelegramGS import *
from services.telegram.TelegramGC import *
from services.telegram.TelegramRABBY import *
from services.CronService import *


def create_app():
    my_app = Flask(__name__)
    return my_app


app = create_app()


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
    if name == 'str':
        docs = TelegramSTR().read()
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
    TelegramRABBY().listen_webhook(d)
    return 'OK'


@app.route('/home')
def home():
    return render_template(
        'home.html',
        config=get_config(),
        groups=['gs', 'test', 'tr2', 'bg88']
    )


@app.route('/send/<name>', methods=['POST'])
def send(name):
    text = request.form.get('text')
    if text:
        TelegramTest().send_message(text)
    return 'OK'


@app.route('/cron/add', methods=['POST'])
def cron_add():
    update = json.loads(s=request.data)
    if update:
        CronService({"chat_id": -320735075}).add(update, {"time": "2019-10-10 10:10:10", "done": 0})
    return 'OK'


@app.route('/cron/list', methods=['POST'])
def cron_list():
    for x in CronService().get_jobs():
        print(x)
    return 'OK'


@app.route('/cron/exec', methods=['POST'])
def cron_exec():
    CronService().exec()
    return 'OK'


@app.route('/bot', methods=['GET'])
def test():
    TelegramBot({}).check_is_webhook_set()
    return 'OK'


@app.template_filter('ts_to_date')
def ts_to_date(ts):
    from datetime import datetime
    import pytz
    utc_moment_naive = datetime.utcfromtimestamp(ts)
    utc_moment = utc_moment_naive.replace(tzinfo=pytz.utc)
    return utc_moment.astimezone(pytz.timezone('Asia/Taipei')).strftime("%Y-%m-%d %H:%M:%S")


@app.route('/')
def index():
    return 'OK'


if __name__ == '__main__':
    app.run()
