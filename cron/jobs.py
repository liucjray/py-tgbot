from flask import Flask
from flask_apscheduler import APScheduler
from repositories.AtlasJobService import *
from services.telegram.TelegramBot import *
from datetime import datetime, timedelta
from dateutil import parser


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'jobs:job_10s',
            'trigger': 'interval',
            'seconds': 10
        }
    ]

    SCHEDULER_API_ENABLED = True


def job_10s():
    bot = TelegramBot({})
    s = AtlasJobService()
    jobs = s.read_jobs()
    for job in jobs:

        sender_name = []
        if dict_get(job, 'message.from.first_name') is not None:
            sender_name.append(dict_get(job, 'message.from.first_name'))
        if dict_get(job, 'message.from.last_name') is not None:
            sender_name.append(dict_get(job, 'message.from.last_name'))
        message_from = ' '.join(sender_name)
        # print(message_from)

        chat_id = dict_get(job, 'message.chat.id')
        message_id = dict_get(job, 'message.message_id')
        cron_text = dict_get(job, 'cron.text')
        cron_time = dict_get(job, 'cron.time')
        dt_cron_time = parser.parse(cron_time)

        # 判斷是否需要發送訊息
        need_send = datetime.now() + timedelta(seconds=-60) < dt_cron_time < datetime.now() + timedelta(seconds=+60)

        if need_send:
            # 發送訊息
            cron_text = "[預約訊息發送] %s: %s" % (message_from, cron_text)
            bot.send_message(chat_id, cron_text)
            print('[%s] Send message job DONE: %s' % (cron_time, cron_text))

            # TODO: 寫入已發送的訊息之後才刪的到
        else:
            continue

        # 發送訊息後更新資料庫
        s.done_jobs(message_id)


if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config())

    scheduler = APScheduler()
    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    app.run()
