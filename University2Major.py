# import pymysql as mdb
# import csv
from Utils import Utils

"""
根据大学与专业列表生成insert sql文
"""


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

    # 大学列表对应ID，只选取本科部分
    sql = 'select a.id, a.university_name from university_list a WHERE a.education_level LIKE "%本科%"'
    university_dic = {}
    for row in Utils.get_data(sql):
        university_dic.update({row[1]: row[0]})
    # print(university_dic)

    # 专业列表，只选取本科部分
    sql = "SELECT major_name,id FROM `university_major_list` a WHERE a.type = 3 AND a.major_level = 1"
    majors_dic = dict(Utils.get_data(sql))
    # for row in get_data(sql):
    #     majors_dic.update({row[0]: row[1]})
    # print(majors_dic)

    result = Utils.read_csv(file)
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


w_data, c_data = make_insert_sql("大学对应专业.csv")

# print(w_data)
Utils.save_to_file(c_data, "大学对应专业SQL.txt")
Utils.save_to_file(w_data, "大学没有对应的专业.txt")

w_data, c_data = make_insert_sql("加逗号.csv")
Utils.save_to_file(c_data, "加逗号SQL.txt")
Utils.save_to_file(w_data, "加逗号-大学没有对应的专业.txt")
