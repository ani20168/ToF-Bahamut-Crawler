import requests
from bs4 import BeautifulSoup
import ctypes
import re
import time,datetime
import os
from playsound import playsound
import threading


#幻塔序號集中串
def concentrate_article_url(article_url):
    if article_url == "https://forum.gamer.com.tw/C.php?bsn=71040&snA=786&tnum=70":
        article_url = "https://forum.gamer.com.tw/C.php?page=20&bsn=71040&snA=786&tnum=70"
    return article_url

#提示音
def play_sound():
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, 'sound.wav')
    if os.path.exists(file_path):
        playsound(file_path)


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
    # 尋找文章元素
    elements = soup.find_all(class_="b-list__row b-list-item b-imglist-item")
    new_articles = []
    for element in elements:
        #尋找文章標題
        title_element = element.find(class_="b-list__main__title")
        for filter in filters:
            if filter in title_element.text:
                # 檢查當前文章是否曾被搜索過
                if title_element.text not in previous_articles:
                    # 印出新文章的標題，標題使用那個原諒的顏色:)
                    ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 2)
                    print("【標題:{}】".format(title_element.text))
                    ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 7)

                    #尋找內文網址
                    article_url = title_element.get("href")
                    article_url = "https://forum.gamer.com.tw/" + article_url
                    #如果是幻塔的序號集中串，則直接進最後一頁
                    article_url = concentrate_article_url(article_url)

                    response = requests.get(article_url,headers=headers)
                    article_soup = BeautifulSoup(response.text, "html.parser")
                    content_elements = article_soup.find_all(class_="c-article__content")
                    for content_element in content_elements:
                        # 匹配 16 位英數字混合亂碼的正規表達式
                        pattern = r'[A-Za-z0-9]{16}'
                        # 使用 findall 方法提取出所有序號
                        codes = re.findall(pattern, content_element.get_text())
                        # 顯示提取出的序號
                        for code in codes:
                            print(code)
                    # Add the current article to the list of previously retrieved articles
                    previous_articles.append(title_element.text)
                    new_articles.append(title_element.text)
                break
    
    if len(new_articles) > 0:
        now = datetime.datetime.now()
        time_str = now.strftime("%m/%d %H:%M")
        print("{} 找到了 {} 篇新文章".format(time_str, len(new_articles)))
        thread = threading.Thread(target=play_sound)
        thread.start()

    time.sleep(30)



