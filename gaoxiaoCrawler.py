import csv
import expangaoxiao as broswer
from bs4 import BeautifulSoup as bs


def get_university_dic():
    return {"university_name": None, "province": None, "belong_to": None, "education_level": None,
            "university_type": None, "university_management_type": None, "is_985": None, "is_211": None,
            "has_graduate_school": None}


def get_url():
    url = "http://gaokao.chsi.com.cn/sch/"

    return url


def get_universities():
    htmls = broswer.get_html(get_url(), True, 3)
    all_university_list = []
    for html in htmls:
        soup = bs(html, "html.parser")
        all_university_list.extend(parse_html(soup))
    return all_university_list


def parse_html(soup):
    left_div = soup.find("div", class_="left")
    tables = left_div.find_all("table")
    university_rows = tables[-1].find_all("tr", bgcolor="#FFFFFF")
    result = []

    for row in university_rows:
        u = get_university_dic()
        tds = row.find_all("td")
        index = 0
        for td in tds:
            if index == 0:
                if len(td.select("span[class='a211985 span985']")) > 0:
                    u["is_985"] = td.select("span[class='a211985 span985']")[0].get_text().strip()
                if len(td.select("span[class='a211985 span211']")) > 0:
                    u["is_211"] = td.select("span[class='a211985 span211']")[0].get_text().strip()
                if len(td.select("span[class='a211985 spanyan']")):
                    u["has_graduate_school"] = td.select("span[class='a211985 spanyan']")[0].get_text().strip()
                if len(td.select("a")) > 0:
                    u["university_name"] = td.select("a")[0].get_text().strip()
                else:
                    u['university_name'] = td.get_text().strip()
            elif index == 1:
                u["province"] = td.get_text().strip()
            elif index == 2:
                u["belong_to"] = td.get_text().strip()
            elif index == 3:
                u["education_level"] = td.get_text().strip().strip()
            elif index == 4:
                u["university_management_type"] = td.get_text().strip()
            elif index == 5:
                u["university_type"] = td.get_text().strip()

            index += 1
        result.append(u)

    return result


def save_file(data, filename="universities.csv"):
    if isinstance(data, list):
        with open(filename, 'w') as f:  # Just use 'w' mode in 3.x
            i = 0
            for row in data:
                w = csv.DictWriter(f, row.keys())

                if i == 0:
                    w.writeheader()
                w.writerow(row)
                i += 1

    print("It's done")


def start_task():
    save_file(get_universities())

# start_task()
