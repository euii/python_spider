from selenium import webdriver
import time
import csv
import expangaoxiao as broswer
from bs4 import BeautifulSoup as bs


# 1.取得所有的专业列表并把专业列表的名称和超链接存入majors.csv
# 2.一行一行读取majors.csv，抓取详细页面并分析出需要的块
# 3.把每页的信息存入字典列表
# 4.输出结果到majors_detail.csv


def get_htmls(url, loadmore=False, waittime=2):
    """
    点击每页下方的下一页按钮
    :param url:
    :param loadmore:
    :param waittime:
    :return:
    """
    browser = webdriver.Chrome('chromedriver')
    browser.get(url)
    time.sleep(waittime)
    result = []
    if loadmore:
        while True:
            try:
                result.append(browser.page_source)
                next_page_button = browser.find_element_by_xpath(
                    "//form[@id='navForm']/div/ul[@class='ulPage']/li[last()]")
                if next_page_button.get_attribute("class") == "lip able":
                    next_page_button.click()
                else:
                    break

                time.sleep(waittime)

            except:
                break

    browser.quit()
    return result


# for test
# url = "http://xz.chsi.com.cn/speciality/index.action"
# html = get_htmls(url, True)
# print(html)


def parse_majors(htmls):
    base_url = "http://xz.chsi.com.cn/"
    all_majors = []
    for html in htmls:
        soup = bs(html, "html.parser")
        rows = soup.find("div", id="div_list").find("table").find("tbody").find_all("tr")
        for row in rows:
            major_name = row.find("td").get_text()
            a = base_url + row.find("td").find("a", href=True)['href']
            all_majors.append({"major_name": major_name, "a": a})

    return all_majors


def save_csv(data, filename="majors_list.csv"):
    if isinstance(data, list):
        with open(filename, 'w') as f:  # Just use 'w' mode in 3.x
            fieldnames = ['major_name', 'a']
            w = csv.DictWriter(f, fieldnames)
            # w.writeheader()
            for row in data:
                w.writerow(row)

    print("It's done")


def get_majors_to_csv():
    url = "http://xz.chsi.com.cn/speciality/index.action"
    htmls = get_htmls(url, True)
    save_csv(parse_majors(htmls))


get_majors_to_csv()
