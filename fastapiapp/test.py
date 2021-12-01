# import pymssql
# # try finding a way to get all the data as a dictionary


# # conn = pymssql.connect(host="DESKTOP-IJ2FP7P", user="raindata5", password="natalia", database="flask_notifications")
# conn = pymssql.connect(host="localhost", user="raindata5", password="natalia", database="flask_notifications")
# # DB_USER="raindata5", DB_PASS="natalia", DB_ADDR=, DB_NAME="flask_notifications")
# if conn:
#     print("got connection")
# else:
#     print("nah")

# query = "SELECT * FROM test"

# cursor = conn.cursor(as_dict=True)
# cursor.execute("SELECT * FROM test").fetchone()
# data = cursor.fetchall()
# conn.close()
