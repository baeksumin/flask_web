import pymysql

db_connection = pymysql.connect(
	user    = 'root',
        passwd  = '12345678',
    	host    = '127.0.0.1',
    	db      = 'gangnam',
    	charset = 'utf8'
)

cursor = db_connection.cursor()

sql = 'SELECT * FROM list;'

cursor.execute(sql)

topics = cursor.fetchall()

print(topics)