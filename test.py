from datetime import timedelta, datetime

# default table
issue_info_shardings = ['issue_info']
issue_info_shardings_exclude = []

for day in range(7, 37):
    # 不抓今天
    target_day = datetime.now() - timedelta(1) - timedelta(day)
    date = datetime.strftime(target_day, '%Y%m%d')

    # 組分表群
    tb = "issue_info_{}".format(str(date))
    # 跳過不要的分表
    if tb in issue_info_shardings_exclude:
        continue
    # 加入分表群
    issue_info_shardings.append(tb)

# 组單一 sql
sqls = []
for tb in issue_info_shardings:
    sql = "SELECT issue, code from {} where lottery_id in (212)".format(tb)
    sqls.append(sql)

# union all 合併
final_sql = " UNION ALL ".join(sqls)

# 外層包覆 sql
final_sql = """
SELECT issue, code FROM ( {} ) t where 1 and code is not null order by issue
""".format(final_sql)

print(final_sql)
