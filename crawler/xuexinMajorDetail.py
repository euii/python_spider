from selenium import webdriver
import time
import csv
from bs4 import BeautifulSoup as bs


def get_html(browser, url, waittime=2):
    # browser = webdriver.Chrome('chromedriver')
    opend = False
    while opend is False:
        try:
            browser.get(url)
            time.sleep(waittime)
            browser.find_element_by_xpath("/html/body/div[2]/div[2]/div")
            result = browser.page_source
            opend = True

        except:
            opend = False

    # browser.quit()
    return result


def read_csv(file):
    with open(file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)

    return reader


def parse_html(html):
    soup = bs(html, "html.parser")
    div = soup.find("div", class_="width1000 bgwhite margintop20 padding20")
    # major_instruction = div.find("p", class_="zymsg clear-both").get_text().strip()
    major_instruction = ""
    major_code = div.select('div[class="warp-jbxx clearfix"] > ul > li')[1].get_text().split("：")[1].strip()

    graduate_work_str, students_hope_works_str, major_course_str = "", "", ""
    # 已毕业人员从业方向
    try:
        graduate_works = div.find("div", id="div_list").find("div", id="occ").select("ul > li > a")
        if isinstance(graduate_works, list):
            graduate_work_str = ' '.join("%s" % item.get_text().strip() for item in graduate_works)
    except:
        pass

    # 在校生期望从业方向
    try:
        students_hope_works = div.find("div", id="div_list").find("div", id="exp_occ").select("ul > li > a")
        if isinstance(students_hope_works, list):
            students_hope_works_str = " ".join("%s" % item.get_text().strip() for item in students_hope_works)
    except:
        pass

    # 开设专业课程
    try:
        major_courses = div.find("table", class_="myd tabmyd").select("tbody > tr > td:nth-of-type(1)")
        if isinstance(major_courses, list):
            major_course_str = "|".join("%s" % item.get_text().strip() for item in major_courses)
    except:
        pass

    return {"major_instruction": major_instruction, "major_code": major_code, "graduate_work_str": graduate_work_str,
            "students_hope_works_str": students_hope_works_str, "major_course_str": major_course_str}


def save_major_detail_to_csv(file, start_step=0):
    result = []
    browser = webdriver.Chrome('chromedriver')
    with open(file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        i = 0
        with open("majors_detail_2.csv", "w") as f:
            fieldnames = ['major_name', 'major_code', "major_instruction", "graduate_work_str",
                          "students_hope_works_str", "major_course_str"]
            w = csv.DictWriter(f, fieldnames)
            w.writeheader()
            for row in reader:

                if i >= start_step:
                    major_name, url = (row[0], row[1])
                    print("No. {} fetch {} ".format(i, major_name))
                    major_detail = parse_html(get_html(browser, url))
                    major_detail['major_name'] = major_name
                    w.writerow(major_detail)

                    # result.append(major_detail)
                i += 1
                # if i == 10:
                #     break
        # save_csv(result)
    browser.quit()


def save_csv(data, filename="majors_detail.csv"):
    if isinstance(data, list):
        with open(filename, 'w') as f:  # Just use 'w' mode in 3.x
            fieldnames = ['major_name', 'major_code', "major_instruction", "graduate_work_str",
                          "students_hope_works_str", "major_course_str"]
            w = csv.DictWriter(f, fieldnames)
            w.writeheader()
            for row in data:
                w.writerow(row)

    print("It's done")


# test
# html = get_html("http://xz.chsi.com.cn/speciality/detail.action?specId=izvb457dyz932ywg")
# parse_html(html)
# print(parse_html(html))
save_major_detail_to_csv("majors_list.csv", 0)
