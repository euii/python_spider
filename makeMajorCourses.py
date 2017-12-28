import csv


def read_csv(file):
    result = []
    with open(file, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)  # pass csv header
        for row in reader:
            major_code, major_course = row[0], row[1]
            if major_course == "暂时没有收录到课程，请补充！":
                continue
            else:
                course_list = major_course.split("|")
                for course in course_list:
                    result.append([major_code, course])
    return result


def save_data_to_sql(data):
    with open("major_course.sql", "w") as sql:
        sql.write("INSERT INTO `wxudf`.`university_major_course` (`major_code`, `major_course_name`) VALUES\n")
        for row in data:
            sql.write("(" + ",".join("'%s'" % item for item in row) + "),\n")


data = read_csv("major_course.csv")
save_data_to_sql(data)
