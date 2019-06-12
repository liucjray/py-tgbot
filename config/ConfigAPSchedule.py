from apscheduler.jobstores.mongodb import MongoDBJobStore


class Config(object):
    pass
    # JOBS = [
    #     {
    #         'id': 'job1',
    #         'func': 'advanced:job1',
    #         'args': (1, 2),
    #         'trigger': 'interval',
    #         'seconds': 10
    #     }
    # ]
    #
    # SCHEDULER_JOBSTORES = {
    #     'default': MongoDBJobStore(url='sqlite://')
    # }
    #
    # SCHEDULER_EXECUTORS = {
    #     'default': {'type': 'threadpool', 'max_workers': 20}
    # }
    #
    # SCHEDULER_JOB_DEFAULTS = {
    #     'coalesce': False,
    #     'max_instances': 3
    # }
    #
    # SCHEDULER_API_ENABLED = True
