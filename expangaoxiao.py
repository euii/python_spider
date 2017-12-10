from selenium import webdriver
import time





"""
url: the gaokao.chsi.com.cn page we will get html from
loadmore: whether or not click load more on the bottom 
waittime: seconds the broswer will wait after intial load and 
"""


def get_html(url, loadmore=False, waittime=2):
    browser = webdriver.Chrome('chromedriver')
    browser.get(url)
    time.sleep(waittime)
    result = [browser.page_source]
    if loadmore:
        while True:
            try:
                # last_li = browser.find_element_by_xpath("//form[@id='PageForm']/ul[@class='ulPage']/li[last()]")
                next_page_button = browser.find_element_by_xpath(
                    "//form[@id='PageForm']/ul[@class='ulPage']/li[last()]/a")

                # if last_li.get_attribute("class") != "lip unable":
                #     next_page_button.click()
                # else:
                #     return None
                next_page_button.click()
                time.sleep(waittime)
                result.append(browser.page_source)

            except:
                break
                # browser.quit()
                # return None
    # html = browser.page_source
    browser.quit()
    return result

# for test
# url = "http://gaokao.chsi.com.cn/sch/"
# url = "http://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-2640.dhtml"
# html = get_html(url, True)
# print(html)
