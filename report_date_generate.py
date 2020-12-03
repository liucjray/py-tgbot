import time
from datetime import timedelta, datetime

# for x in range(0, 1000):
#     date = datetime.strftime(datetime.now() - timedelta(x), '%Y-%m-%d')
#     sql = "INSERT INTO report_dates(date) VALUES ('{}');".format(date)
#     print(sql)

weeks = []
weekdays = []
for x in range(0, 300):
    week = int(datetime.strftime(datetime.now() + timedelta(x), '%V'))
    date = datetime.strftime(datetime.now() + timedelta(x), '%Y-%m-%d')
    weekday = datetime.strptime(date, '%Y-%m-%d').weekday() + 1

    if weekday == 1:
        week = week + 1
        weekdays = weekdays and weekdays.append(date) or [date]
        weeks.append({week: weekdays})
    if weekday == 7:
        weekdays = weekdays and weekdays.append(date) or [date]
        weeks.append({week: weekdays})

    sql = "{}, {}, {}".format(week, date, weekday)

    print(weeks)
    print(sql)
