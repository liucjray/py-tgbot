from flask import Flask, render_template, request, send_from_directory

from services.telegram.TelegramSTR import *
from services.telegram.TelegramTR2 import *
from services.telegram.TelegramBG88 import *
from services.telegram.TelegramTest import *
from services.telegram.TelegramGS import *
from services.telegram.TelegramGC import *
from services.telegram.TelegramRABBY import *
from services.telegram.TelegramADMIN import *
from services.CronService import *


def create_app():
    my_app = Flask(__name__)
    return my_app


app = create_app()


@app.route('/set_webhook')
def set_webhook():
    msg = TelegramTest().set_webhook()
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
    TelegramADMIN().listen_webhook(d)
    print(d)
    return 'OK'


@app.route('/')
def index():
    return 'OK'


@app.route('/home')
def home():
    return render_template(
        'home.html',
        config=get_config(),
        groups=['gs', 'test', 'tr2', 'bg88']
    )


@app.route('/read/<name>')
def read(name):
    docs = telegram_mapper(name).read()
    return render_template(
        'telegram/read.html',
        docs=docs
    )


@app.route('/cron/read/<name>', methods=['GET'])
def cron_list(name):
    instance = telegram_mapper(name)
    crons = CronService().get_jobs(chat_id=instance.chat_id)
    return render_template(
        'cron/read.html',
        crons=crons
    )


@app.route('/cron/add', methods=['POST'])
def cron_add():
    update = json.loads(s=request.data)
    if update:
        CronService({"chat_id": -320735075}).add(update, {"time": "2019-10-10 10:10:10", "done": 0})
    return 'OK'


@app.route('/cron/del', methods=['POST'])
def cron_del():
    _id = dict_get(json.loads(s=request.data), 'id', None)
    CronService().del_job(_id=_id)
    return 'ok'


@app.template_filter('ts_to_date')
def ts_to_date(ts):
    from datetime import datetime
    import pytz
    utc_moment_naive = datetime.utcfromtimestamp(ts)
    utc_moment = utc_moment_naive.replace(tzinfo=pytz.utc)
    return utc_moment.astimezone(pytz.timezone('Asia/Taipei')).strftime("%Y-%m-%d %H:%M:%S")


@app.template_filter('time_format')
def time_format(t):
    y = t[0:4]
    m = t[4:6]
    d = t[6:8]
    h = t[8:10]
    i = t[10:12]
    s = t[12:14]
    return '-'.join([y, m, d]) + ' ' + ':'.join([h, i, s])


def telegram_mapper(name):
    instance = None
    if name == 'test':
        instance = TelegramTest()
    if name == 'bg88':
        instance = TelegramBG88()
    if name == 'tr2':
        instance = TelegramTR2()
    if name == 'gs':
        instance = TelegramGS()
    if name == 'gc':
        instance = TelegramGC()
    if name == 'str':
        instance = TelegramSTR()
    if name == 'rabby':
        instance = TelegramRABBY()
    if name == 'admin':
        instance = TelegramADMIN()
    return instance


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join('static'), 'favicon.ico')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
