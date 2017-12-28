import re


def read_file(file):
    result = []
    with open(file, 'r') as f:
        code, major = "", ""
        for row in f:
            r = row.strip().split(",")
            if r[0] == "" or r[1] == "":
                pattern = re.compile(r"^\d")
                match = pattern.match(r[0])
                if match:
                    code = match.string
                else:
                    major = r[0]
            if code != "" and major != "":
                result.append({code: major})
                code, major = "", ""
    return result


def save_file(data, file):
    with open(file, "w") as f:
        for row in data:
            for key in row:
                f.write("{},{}\n".format(key, row[key]))


result = read_file("教育部专业目录.txt")
save_file(result, "教育专业目录1.txt")
