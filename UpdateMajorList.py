from UniversityMajor import get_data
from UniversityMajor import read_csv


def make_data_dic():
    sql = "SELECT major_code FROM university_major_list"

    data = get_data(sql)
    code_dic = {}
    for row in data:
        key = row[0]
        code_dic.update({key: "1"})
    return code_dic


def make_new_data(code_dic):
    result = {}
    file_data = read_csv("教育部专业目录.txt")

    for row in file_data:
        row_data = row.strip().split(",")
        if code_dic.get(row_data[0]) is None:
            result.update({row_data[0]: row_data[1]})

    return result


def save_file(data, file):
    with open(file, "w") as f:
        f.write("INSERT INTO `wxudf`.`university_major_list` (`major_code`, `major_name`, `type`,`p_id`) VALUES \n")
        for row in data:
            type = -1
            p_id = -1

            code_len = len(row)
            if code_len == 2:
                type = 1
                p_id = 0
            elif code_len == 4:
                type = 2
            elif code_len >= 6:
                type = 3
            f.write("('{}','{}',{},{}),\n".format(row, data[row], type, p_id))


dic = make_data_dic()

# print(dic)

result = make_new_data(dic)

# print(result)

save_file(result, "专业目录新数据1.txt")
