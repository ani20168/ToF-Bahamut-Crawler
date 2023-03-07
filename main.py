import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
import os
import threading
from playsound import playsound
import webhook

# 定義常數
URL = "https://forum.gamer.com.tw/B.php?bsn=71040" #要爬取的哈拉版
FILTERS = ["虛寶", "序號", "禮包"]                  #篩選這些標題
FILTERS_IGNORE = ["序號分享及兌換方式"]             #忽略標題
webhook.url = ""                                   #是否使用 Discord 通知? 如需使用，請在這裡新增你的webhook網址
SOUND_FILE_PATH = os.path.join(os.getcwd(), "sound.wav")

# 定義表頭
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

# 定義已搜索過的文章列表
SEARCHED_ARTICLES = []

# 定義提示音函數
def play_sound():
    if os.path.exists(SOUND_FILE_PATH):
        playsound(SOUND_FILE_PATH)

# 定義爬蟲函數
def crawl():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    article_elements = soup.find_all(class_="b-list__row b-list-item b-imglist-item")

    new_articles = []
    for article in article_elements:
        title_element = article.find(class_="b-list__main__title")
        title = title_element.text

        # 過濾文章
        if any(filter in title for filter in FILTERS) and not any(filter in title for filter in FILTERS_IGNORE):
            if title not in SEARCHED_ARTICLES:
                # 新文章，進行處理
                print(f"【標題：{title}】")
                webhook.ContentAdd(title) if webhook.url else None

                article_url = "https://forum.gamer.com.tw/" + title_element.get("href")
                response = requests.get(article_url, headers=HEADERS)
                article_soup = BeautifulSoup(response.text, "html.parser")
                content_elements = article_soup.find_all(class_="c-article__content")

                codes = []
                for content_element in content_elements:
                    # 匹配序號
                    pattern = r"[A-Za-z0-9]{13}"
                    codes.extend(re.findall(pattern, content_element.get_text()))

                # 輸出序號
                for code in codes:
                    print(code)
                    webhook.ContentAdd(code) if webhook.url else None

                # 將已搜索過的文章加入列表
                SEARCHED_ARTICLES.append(title)
                new_articles.append(title)

    if len(new_articles) > 0:
        # 有新文章，提示並發送 Discord 通知
        now = datetime.datetime.now().strftime("%m/%d %H:%M")
        print(f"{now} 找到了 {len(new_articles)} 篇新文章")
        threading.Thread(target=play_sound).start()
        webhook.Post() if webhook.url else None

# 主程式
if __name__ == "__main__":
    print("============")
    print("巴哈哈拉版序號爬蟲")
    print("============")

    while True:
        crawl()
        time.sleep(10)




