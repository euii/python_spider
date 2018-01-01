from Utils import Utils
import csv
import expangaoxiao as browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import pandas as pd


def get_url():
    url = "http://gaokao.chsi.com.cn/sch/"

    return url


# 1.取得高校列表的URL，保存到CSV
def get_universities():
    htmls = browser.get_html(get_url(), True, 3)
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
    base_url = "http://gaokao.chsi.com.cn"

    for row in university_rows:
        tds = row.find_all("td")
        index = 0
        for td in tds:
            if index == 0:
                if len(td.select("a")) > 0:
                    # u["is_985"] = td.select("span[class='a211985 span985']")[0].get_text().strip()
                    result.append(
                        "{},{}".format(td.find("a").get_text().strip(), base_url + td.find("a", href=True)['href']))
                    continue

            index += 1

    return result


# 2.取得高校列表的专业URL，保存到CSV
def get_detail_html_url(wait_time=2):
    browser = webdriver.Chrome('chromedriver')
    data = Utils.read_csv("output/高校详情页URL.csv")
    result = []
    index = 0
    for rows in data:
        row = rows.strip().split(",")
        try:
            browser.get(row[1])
            a = browser.find_element_by_xpath("//div[@class='left']/ul/li[@id='yxxx7']/a").get_attribute("href")
            time.sleep(wait_time)
            row_text = ("{}|{} \n".format(row[0], a))
        except:
            row_text = ("{}|{} \n".format(row[0], "error"))
        finally:
            with open("output/高校专业介绍URL.csv", "a") as f:
                f.write(row_text)
        index += 1
        print(index)
    return result


# 3.打开高校列表的专业详细页，保存到CSV

# 4.展开两级科目到3类专业，并去掉重复


# 1
def start_task_1():
    data = get_universities()
    Utils.save_to_file(data, "output/GaoXiaoZhuanYe.csv")


# 2
def start_task_2():
    data = get_detail_html_url()
    # Utils.save_to_file(data, "output/高校专业介绍URL.csv")


# 执行模块
# start_task_1()
# start_task_2()
