import pymysql as mdb


class Utils:

    def __init__(self):
        pass

    @staticmethod
    def get_data(sql):
        # sql = "SELECT id,province_name FROM wxudf.china_province_list"
        result = []

        try:
            db = mdb.connect('127.0.0.1', 'root', '123456', 'wxudf', charset='utf8')

            # prepare a cursor object using cursor() method
            cursor = db.cursor()

            # Prepare SQL query to INSERT a record into the database.

            # Execute the SQL command
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                result.append(row)
            # Commit your changes in the database
            # db.commit()
        except mdb.Error:
            # Rollback in case there is any error
            db.rollback()

            # disconnect from server
        finally:
            if db:
                db.close()

            return result

    @staticmethod
    def save_to_file(data, file, file_mode="w"):
        with open(file, file_mode) as f:
            for row in data:
                f.write(row + "\n")

    @staticmethod
    def read_csv(file):
        result = []
        with open(file, 'r') as f:
            for row in f:
                result.append(row)

        return result
