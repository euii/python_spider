import MySQLdb as mdb
import csv

"""
根据大学与专业列表生成insert sql文
"""

def get_data(sql):
    # sql = "SELECT id,province_name FROM wxudf.china_province_list"
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


def read_csv(file):
    result = []
    with open(file, 'r') as f:
        # reader = csv.reader(f)

        # for row in reader:
        #     print(row)
        # return reader
        index = 0
        for row in f:
            result.append(row)

    return result


def find_dividing_line(list):
    """
    找一行两个及以上的|线
    :return:
    """
    index = 1
    for row in list:
        count = row.count("|")
        if (count == 0):
            print("第{}行,有{}个| ".format(index, count))
        index += 1


def make_insert_sql(file):
    """
    生成大学对应专业的SQL
    :return:
    """
    wrong_data = []
    corrent_sql = []

    # 大学列表对应ID
    sql = "select a.id, a.university_name from university_list a"
    university_dic = {}
    for row in get_data(sql):
        university_dic.update({row[1]: row[0]})
    # print(university_dic)

    # 专业列表
    sql = "SELECT major_name,id FROM `university_major_list`"
    majors_dic = dict(get_data(sql))
    # for row in get_data(sql):
    #     majors_dic.update({row[0]: row[1]})
    # print(majors_dic)

    result = read_csv(file)
    insert_sql = 'INSERT INTO `wxudf`.`university_has_major` (`university_list_id`, `university_major_list_id`, `is_cooperation`) VALUES ({},{},{});'
    for row in result:

        row_data = row.strip().split("|")
        university_name = row_data[0].strip()
        university_id = university_dic.get(university_name)
        if university_id is None:
            wrong_data.append("{}|".format(university_name))
            continue
        else:
            majors = row_data[1].split(",")
            for major in majors:
                major = major.strip()
                is_cooperation = 0
                index = major.find("(中外合作办学)")
                if index > -1:
                    is_cooperation = 1
                    major = major[0:index]
                    # print("中外合作 {}".format(major))

                major_id = majors_dic.get(major)
                if major_id is None:
                    wrong_data.append("{}|{}".format(university_name, major))
                else:
                    corrent_sql.append(insert_sql.format(university_id, major_id, is_cooperation))

    return wrong_data, corrent_sql


def save_to_file(data, file):
    with open(file, "w") as f:
        for row in data:
            f.write(row + "\n")


w_data, c_data = make_insert_sql("大学对应专业.csv")

# print(w_data)
save_to_file(c_data, "大学对应专业SQL.txt")
save_to_file(w_data, "大学没有对应的专业.txt")

w_data, c_data = make_insert_sql("加逗号.csv")
save_to_file(c_data, "加逗号SQL.txt")
save_to_file(w_data, "加逗号-大学没有对应的专业.txt")
