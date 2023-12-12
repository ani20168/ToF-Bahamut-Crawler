import requests
from bs4 import BeautifulSoup
import re
import ctypes
import time
import datetime
import os
import threading
from playsound import playsound
import webhook


url = "https://forum.gamer.com.tw/B.php?bsn=71040" #要爬取的哈拉版
filters = ["虛寶", "序號", "禮包"]                  #篩選這些標題
filters_ignore = ["序號分享及兌換方式"]             #忽略標題
webhook.url = ""                                   #是否使用 Discord 通知? 如需使用，請在這裡新增你的webhook網址
sound_path = os.path.join(os.getcwd(), "sound.wav")

# 定義表頭
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

# 已搜索過的序號
scarched_codes = []

def play_sound():
    if os.path.exists(sound_path):
        playsound(sound_path)

# 匹配一頁的序號
def find_code_in_page(content_elements) -> list:
    codes = []
    pattern = r"\b([A-Za-z0-9]{17}|[A-Za-z0-9]{16}|[A-Za-z0-9]{13})\b"
    for content_element in content_elements:
        matches = re.finditer(pattern, str(content_element))
        codes.extend(match.group(1) for match in matches if match.group(1))
    return codes

#檢查文章是否有多頁
def multipage_check(article_element):
    title_element = article_element.find(class_="b-list__main__title")
    article_url = "https://forum.gamer.com.tw/" + title_element.get("href")

    # 檢查是否有多頁，如果是，找出最後一頁的網址
    pages_element = article_element.find(class_="b-list__main__pages")
    if pages_element:
        article_url = "https://forum.gamer.com.tw/" + pages_element.find_all("span")[-1].get("data-page")
        
    return article_url

# 主程式
def main():
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
    except (requests.exceptions.Timeout, requests.exceptions.RequestException):
        # 處理請求超時或者連接錯誤等異常
        print(f"{datetime.datetime.now().strftime('%m/%d %H:%M:%S')} 請求失敗")
        return
        
    article_elements = soup.find_all(class_="b-list__row b-list-item b-imglist-item")

    new_articles = []
    for article in article_elements:
        title_element = article.find(class_="b-list__main__title")
        title = title_element.text
        #要求文章網址
        article_url = multipage_check(article)

        
        # 過濾文章
        if any(filter in title for filter in filters) and not any(filter in title for filter in filters_ignore):

            response = requests.get(article_url, headers=HEADERS)
            article_soup = BeautifulSoup(response.text, "html.parser")
            content_elements = article_soup.find_all(class_="c-article__content")

            codes_in_page = find_code_in_page(content_elements)
            #刪除已搜索過的序號
            codes_in_page = [code for code in codes_in_page if code not in scarched_codes]

            # 輸出找到的新序號
            if codes_in_page:
                ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 2) #變更標題顏色
                print(f"【標題：{title}】")             
                webhook.ContentAdd(title) if webhook.url else None

                print(f"【網址：{article_url}】")
                webhook.ContentAdd(article_url) if webhook.url else None
                ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 7)

                for code in codes_in_page:
                    print(code)
                    webhook.ContentAdd(code) if webhook.url else None
                    #將序號加入已搜索名單
                    scarched_codes.append(code)

                new_articles.append(len(codes_in_page))

    if len(new_articles) > 0:
        # 有新文章，提示並發送 Discord 通知
        now = datetime.datetime.now().strftime("%m/%d %H:%M")
        print(f"{now} 找到了 {len(new_articles)} 篇新文章，共 {sum(new_articles)} 筆新序號")
        try:
            threading.Thread(target=play_sound).start()
        except:
            pass
        webhook.Post() if webhook.url else None

# 主程式
if __name__ == "__main__":
    print('''
    ==================
    巴哈哈拉版序號爬蟲
    ==================''')

    while True:
        main()
        time.sleep(10)




