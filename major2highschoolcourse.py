from Utils import Utils
import time

"""
这个文件作废
"""


class RemoveOpenBrace:

    def __init__(self):
        pass

    def read_file(self, file):
        with open(file, 'r') as f:
            result = []
            for row in f:
                row_list = row.strip().split(",")
                major = row_list[0]
                if major.find("(") > -1 and major.find("(中外合作办学)") == -1:
                    left = major.find("(")
                    right = major.find(")")
                    row_list[0] = major[0:left][-right:]
                    row = ",".join(row_list)
                result.append(row)
        return result

    def save_file(self, data, file):
        with open(file, "w") as f:
            for row in data:
                f.write(row.strip() + "\n")


class FindCorrectData:
    def __init__(self):
        pass

    @staticmethod
    def get_majors_data():
        sql = 'SELECT major_name,id FROM university_major_list a WHERE is_del = 0 AND `type` IN (2,3)'

        return dict(Utils.get_data(sql))

    @staticmethod
    def split_data(dict_data):
        correct_list, wrong_list = [], []
        data_list = Utils.read_csv("高校招生专业要求去括号版0905.csv")
        for row in data_list:
            row_array = row.strip().split(",")
            major = row_array[0].strip().replace("(中外合作办学)", "")

            if dict_data.get(major):
                correct_list.append(row.strip())
            else:
                wrong_list.append(row.strip())
        Utils.save_to_file(correct_list, "高校招生专业目录（正确）.csv")
        Utils.save_to_file(wrong_list, "高校招生专业目录（错误）.csv")

    @staticmethod
    def remove_unlimited_data(file):
        result = []
        data_list = Utils.read_csv(file)
        for data in data_list:
            if data.find("不限") > -1:
                pass
            else:
                result.append(data.replace("(中外合作办学)", ""))
        return result

    @staticmethod
    def generate_sql(file):
        correct_data, wrong_data = [], []
        # 大学专业列表
        sql = 'SELECT concat(a.university_name, b.major_name) as `key`, c.id FROM university_list a, university_major_list b, ' \
              'university_has_major c WHERE a.id = c.university_list_id AND b.id = c.university_major_list_id'

        data_dict = dict(Utils.get_data(sql))

        # 高校列表
        high_courses = {"物理": "1", "化学": "2", "生物": "3",
                        "思想政治": "4", "历史": "5", "地理": "6", "技术": "7"}

        data_list = Utils.read_csv(file)
        sql = "INSERT INTO `university_has_major_has_school_course` (`university_has_major_id`, `high_school_course_id`) VALUES "
        i = 1
        for row in data_list:
            data = row.strip().split(",")
            major, courses_text, university = data[0].strip(
            ), data[1].strip(), data[2].strip()
            u_m_id = data_dict.get(university + major)

            for c_row in courses_text.split("、"):
                h_id = high_courses.get(c_row.strip())
                if u_m_id is not None and h_id is not None:
                    correct_data.append("({},{}),".format(u_m_id, h_id))
                else:
                    wrong_data.append(row)
                    break
            i += 1
        correct_data.insert(0, sql)
        return correct_data, wrong_data


# 前置步骤 把整个目录的大专和本科分开


# # 第一步格式化数据，去掉括号内专业
r = RemoveOpenBrace()
data = r.read_file("高校招生专业要求 0905.csv")
r.save_file(data, "高校招生专业要求去括号版0905.csv")
#
# # 第二步 查找专业是否匹配
time.sleep(2)
data_dict = FindCorrectData.get_majors_data()
FindCorrectData.split_data(data_dict)

# 第三步 去除专业为"不限"的数据
time.sleep(2)
expand_data = FindCorrectData.remove_unlimited_data("高校招生专业目录（正确）.csv")
r.save_file(expand_data, "高校招生专业目录（正确）去掉不限.csv")

# 第四步 生成sql
time.sleep(2)
c_data, w_data = FindCorrectData.generate_sql("高校招生专业目录（正确）去掉不限.csv")
r.save_file(c_data, "高校专业目录SQL.txt")
r.save_file(w_data, "高校专业目录SQL-错误.txt")
