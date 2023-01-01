# ToF Bahamut Crawler
![image](https://github.com/ani20168/ToF-Bahamut-Crawler/blob/main/ReadmeImage.png)

在巴哈姆特幻塔的哈拉版上爬來爬去，把序號爬出來  
有爬到新的文章，會有音效提示，所以可以安心放在後台不用怕漏掉  
上面的是最初版本，更新後我把編號功能拿掉了，這樣在複製序號時比較方便  
預設是篩選"序號"、"虛寶"、"禮包"這三個文章標題  

## 使用
`pip install -r requirements.txt --upgrade`

## 改爬其他哈拉版的序號
1.request.get改成你要爬的哈拉版  
2.幻塔序號集中串那一段可以註解掉(用不到)  
3.正則表達式改成你想爬的序號格式(在幻塔是16位數英數字混合亂碼)
