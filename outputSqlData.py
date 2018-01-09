import pymysql as mdb


def get_provinces():
    sql = "SELECT id,province_name FROM wxudf.china_province_list"
    result = []

    try:
        db = mdb.connect('127.0.0.1', 'wxudf', 'wxudf', 'wxudf', charset='utf8')

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # Prepare SQL query to INSERT a record into the database.

        # Execute the SQL command
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            result.append({row[1]: row[0]})
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


def read_file(data_file):
    sql_prefix = "INSERT INTO `wxudf`.`university_list` (`id`, `university_type`, `belong_to`, `province`, `address`, " \
                 "`university_site_url`, `contact_number`, `special_enrollment`, `admissions_professional`, " \
                 "`university_introduction`, `admissions_url`, `is_del`, `create_time`, `update_time`, " \
                 "`create_user`, `update_user`, `order_number`, `china_province_list_id`, `is_985`, `is_211`, " \
                 "`has_graduate_school`, `education_level`, `university_type`, `university_management_type`, " \
                 "`university_name`) VALUES ("
    result = dict()
    with open(data_file, 'r') as f:
        for line in f:
            row_list = line.strip().split(',')
            location = row_list[2]
            category = row_list[3]
            if category in result:
                if location in result[category]:
                    result[category][location] += 1
                else:
                    result[category][location] = 1
            else:
                result[category] = {location: 1}
    return result
