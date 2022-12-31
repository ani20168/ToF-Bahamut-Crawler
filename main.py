import requests
from bs4 import BeautifulSoup
import ctypes
import re
import time

#表頭
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

#篩選列表
filters = ["虛寶", "序號", "禮包"]

# 顯示過的文章
previous_articles = []


while True:
    # 使用 requests 套件請求目標網站的 HTML 頁面
    response = requests.get("https://forum.gamer.com.tw/B.php?bsn=71040",headers=headers)

    # 將 HTML 頁面轉換成 BeautifulSoup 物件
    soup = BeautifulSoup(response.text, "html.parser")
    # Retrieve the list of articles
    elements = soup.find_all(class_="b-list__row b-list-item b-imglist-item")
    new_articles = []
    for element in elements:
        title_element = element.find(class_="b-list__main__title")
        for filter in filters:
            if filter in title_element.text:
                # Check if the current article has already been retrieved
                if title_element.text not in previous_articles:
                    # Print the title and content of the new article
                    ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 2)
                    print("【標題:{}】".format(title_element.text))
                    ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 7)
                    article_url = title_element.get("href")
                    article_url = "https://forum.gamer.com.tw/" + article_url
                    response = requests.get(article_url,headers=headers)
                    article_soup = BeautifulSoup(response.text, "html.parser")
                    content_elements = article_soup.find_all(class_="c-article__content")
                    for content_element in content_elements:
                        # 匹配 16 位英數字混合亂碼的正規表達式
                        pattern = r'[A-Za-z0-9]{16}'
                        # 使用 findall 方法提取出所有序號
                        codes = re.findall(pattern, content_element.get_text())
                        # 將提取出的序號條列式顯示
                        for i, code in enumerate(codes):
                            print("{}.{}".format(i + 1, code))
                    # Add the current article to the list of previously retrieved articles
                    previous_articles.append(title_element.text)
                    new_articles.append(title_element.text)
                break
    # If new articles were found, print the number of new articles found
    if len(new_articles) > 0:
        print("找到 {} 篇新文章: {}".format(len(new_articles), ", ".join(new_articles)))
    # If no new articles were found, print a message
    else:
        print("沒有找到新文章")
    time.sleep(30)



