from Utils import Utils
import time


def get_file_data(file):
    return Utils.read_csv(file)


def get_university_detail(data):
    result = []
    for row in data:
        row_list = row.strip().split(",")
        try:
            result.append({"u_name": row_list[0].strip(), "c1": row_list[1].strip(), "c2": row_list[2].strip(),
                           "c3": row_list[3].strip()})
        except:
            print(row)
    return result


def get_university_data():
    sql = "select university_name,id from university_list"
    return dict(Utils.get_data(sql))


def general_sql(file):
    sql = "update university_list set contact_number = '{}', university_site_url='{}',  special_enrollment='{}' WHERE id = {};"
    output = []
    db_data = get_university_data()
    data = get_file_data(file)
    result = get_university_detail(data)
    for row in result:
        u_id = db_data.get(row.get('u_name'))
        if u_id is None:
            print(row.get('u_name'))
        else:
            output.append(sql.format(row.get("c1").strip(), row.get("c2").strip(), row.get("c3").strip(), u_id))
    return output


# insert_sql = general_sql("files/总表revised 1.csv")
# Utils.save_to_file(insert_sql, "output/高校地址－更新.sql")

insert_sql = general_sql("files/总表-特殊招生.csv")
Utils.save_to_file(insert_sql, "output/高校特殊招生－更新.sql")
