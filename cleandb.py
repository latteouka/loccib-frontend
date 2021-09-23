import pymysql
import pymysql.cursors

import time
from datetime import datetime,timezone,timedelta
from datetime import date
import datetime


dt1 = datetime.datetime.utcnow().replace(tzinfo=timezone.utc)
dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區

timenow = dt2.strftime("%Y-%m-%d %H:%M:%S")

dt3 = dt2 - datetime.timedelta(days=30)

time_limit = dt3.strftime("%Y-%m-%d %H:%M:%S")

print(time_limit)

connection = pymysql.connect(host=os.environ.get('CLEARDB_DATABASE_HOST'),
                             user=os.environ.get('CLEARDB_DATABASE_USER'),
                             password=os.environ.get('CLEARDB_DATABASE_PASSWORD'),
                             db=os.environ.get('CLEARDB_DATABASE_DB'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cursor:

	sql = "DELETE FROM `records` WHERE `time`<%s"
    cursor.execute(sql, (time_limit))

    cursor.close()
connection.commit()