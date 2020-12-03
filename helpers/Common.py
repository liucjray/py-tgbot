def get_caller(show=False):
    import inspect
    stack = inspect.stack()
    the_class = stack[1][0].f_locals["self"].__class__.__name__
    the_method = stack[1][0].f_code.co_name
    show and print("  I was called by {}.{}()".format(str(the_class), the_method))
    return the_class, the_method


def object_get(obj, dotted_key, default=None):
    import functools
    try:
        return functools.reduce(getattr, dotted_key.split('.'), obj)
    except AttributeError:
        return default


def dict_get(dictionary, dotted_key, default=None):
    import functools
    keys = dotted_key.split('.')
    try:
        return functools.reduce(lambda d, key: d.get(key) if d else default, keys, dictionary)
    except AttributeError:
        return default


def check_job_time_format(input_time):
    try:
        sample_time14 = '20190102030405'  # 14
        sample_time12 = '201901020304'  # 12

        if len(input_time) not in [len(sample_time14), len(sample_time12)]:
            return False

        if not input_time.isdigit():
            return False

        month = input_time[4:6]
        day = input_time[6:8]
        hour = input_time[8:10]
        minute = input_time[10:12]

        if int(month) not in range(1, 13):
            return False
        if int(day) not in range(1, 32):
            return False
        if int(hour) not in range(0, 24):
            return False
        if int(minute) not in range(0, 60):
            return False

        if len(input_time) == len(sample_time14):
            second = input_time[12:14]
            if int(second) not in range(0, 60):
                return False

        return True
    except Exception as e:
        return False
