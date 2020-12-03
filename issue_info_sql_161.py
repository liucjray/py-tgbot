from datetime import datetime, timedelta

# default table
issue_info_shardings = ['issue_info']

# date range table
today = datetime.today()
for x in range(8, 300):
    delta = timedelta(days=x)
    time_x = today - delta
    tb = "issue_info_{}".format(time_x.strftime('%Y%m%d'))
    issue_info_shardings.append(tb)

# # 组單一 sql
sqls = []
for tb in issue_info_shardings:
    sql = " SELECT issue, code " + \
          " FROM {} " + \
          " WHERE lottery_id in (161) " + \
          "".format(tb)
    sqls.append(sql)

# union all 合併
final_sql = "\n   UNION ALL \n".join(sqls)

# 外層包覆 sql
final_sql = """
SELECT issue, code FROM ( \n {} \n ) t where 1 and code is not null order by issue
""".format(final_sql)

print(final_sql)
