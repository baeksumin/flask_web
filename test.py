# import pymysql

# db_connection = pymysql.connect(
# 	user    = 'root',
#         passwd  = '12345678',
#     	host    = '127.0.0.1',
#     	db      = 'gangnam',
#     	charset = 'utf8'
# )

# cursor = db_connection.cursor()

# sql = 'SELECT * FROM list;'

# cursor.execute(sql)

# topics = cursor.fetchall()

# print(topics)

from passlib.hash import pbkdf2_sha256

hash = pbkdf2_sha256.hash("1234")
print(hash)

result = pbkdf2_sha256.hash("1234")

