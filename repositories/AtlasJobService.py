from repositories.AtlasService import *


class AtlasJobService(AtlasService):
    def __init__(self):
        settings = {
            'collection': 'cron'
        }
        super(AtlasJobService, self).__init__(settings)

    def read_jobs(self):
        where = {'cron.done': 0}
        return self.find(where)

    def done_jobs(self, message_id):
        where = {'message.message_id': int(message_id)}
        update = {'$set': {'cron.done': 1}}
        self.update(where=where, update=update)
