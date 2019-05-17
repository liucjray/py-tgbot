import configparser

from flask import Flask
from pymongo import MongoClient
import telegram
from telegram.ext import (Updater, CommandHandler)

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

app = Flask(__name__)


def get_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def get_bot(token=None):
    config = get_config()
    if token is None:
        token = config['TG']['ACCESS_TOKEN_GYOABOT']
    bot = telegram.Bot(token=token)
    return bot


@app.route('/read/updates')
def read_updates():
    bot = get_bot()
    updates = bot.get_updates()
    # print([u.message.text for u in updates])
    return updates


def get_updater():
    config = get_config()
    return Updater(token=config['TG']['ACCESS_TOKEN_GYOABOT'], use_context=True)


def get_dispatcher():
    updater = get_updater()
    return updater.dispatcher


def get_mongo_tr2():
    config = get_config()
    client = MongoClient(config['MONGODB']['CONNECTION_ATLAS'])
    mongodb_atlas = client.get_database(config['MONGODB']['DB'])
    return mongodb_atlas.tr2


def get_mongo_bg88():
    config = get_config()
    client = MongoClient(config['MONGODB']['CONNECTION_ATLAS'])
    mongodb_atlas = client.get_database(config['MONGODB']['DB'])
    return mongodb_atlas.bg88


@app.route('/write/tr2')
def write_tr2():
    config = get_config()
    mongo = get_mongo_tr2()

    try:
        chat_history = read_updates()
        prepares = write_prepare(chat_history, config['TG']['CHAT_ID_TR2'])
        mongo.insert_many(prepares, ordered=False)
    except Exception as e:
        print(e)
    finally:
        return 'OK'


@app.route('/delete/tr2')
def delete_tr2():
    mongo = get_mongo_tr2()
    bot = get_bot()
    try:
        for r in mongo.find():
            # before delete
            text = r['message']['text']
            is_deleted = r['is_deleted']
            if int(is_deleted) == 1:
                print('text: ' + text + ' has been deleted.')
                continue

            # delete telegram message
            update_id = r['update_id']
            chat_id = r['message']['chat']['id']
            message_id = r['message']['message_id']
            try:
                b = bot.delete_message(chat_id, message_id)
                # 删除成功
                if b is True:
                    mongo.update_one({'update_id': update_id}, {'$set': {'is_deleted': 1}})
            except Exception as e:
                # 刪除失敗
                mongo.update_one({'update_id': update_id}, {'$set': {'is_deleted': 1}})
                print(str(e) + '... message_id: ' + str(message_id))
    except Exception as e:
        print(e)
    finally:
        return 'OK'


def write_prepare(chat_history, chat_id):
    prepares = []
    for update in chat_history:
        if int(update.message.chat.id) == int(chat_id):
            row = update.to_dict()
            prepares.append(row)
    return prepares


@app.route('/write/bg88')
def write_bg88():
    config = get_config()
    mongo = get_mongo_bg88()

    try:
        chat_history = read_updates()
        prepares = write_prepare(chat_history, config['TG']['CHAT_ID_BG88'])
        mongo.insert_many(prepares, ordered=False)
    except Exception as e:
        print(e)
    finally:
        return 'OK'


@app.route('/delete/bg88')
def delete_bg88():
    mongo = get_mongo_bg88()
    bot = get_bot()
    try:
        for r in mongo.find():
            # delete telegram message
            update_id = r['update_id']
            chat_id = r['message']['chat']['id']
            message_id = r['message']['message_id']
            try:
                bot.delete_message(chat_id, message_id)
            except Exception as e:
                # 刪除失敗
                mongo.update_one({'update_id': r['update_id']}, {'$set': {'is_deleted': 1}})
                print(str(e) + '... message_id: ' + str(message_id))
    except Exception as e:
        print(e)
        pass
    finally:
        return 'OK'


if __name__ == '__main__':
    app.run()
