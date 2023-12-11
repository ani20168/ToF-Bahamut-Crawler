import pytest
import sys
from bs4 import BeautifulSoup

sys.path.append('..')

from main import find_code_in_page,multipage_check


def test_find_code_in_page():
    test_cases = [
        (['123456'], []),
        (['你好123'], []),
        (['這是序號:1234567890ABCDEF'], ['1234567890ABCDEF']),
        (['序號1:12345678901234567 序號2:9876543210123456','序號3:1234567890ABC'], ['12345678901234567', '9876543210123456','1234567890ABC']),
        (['<div bgcolor="#FFFFFF"><font color="#192A3D"><font size="3">8/10<br>MIA520<br>GO666<br>WAKU777<br>GOLD888<br>ILOVEHT888</font></font></div>'], []),
        (['''<tbody><tr>
            <td>序號</td>
            <td>9136625DKITZQIJB /</td>
            </tr>
            <tr>
            <td>序號</td>
            <td>3872753DKKDIVCQE /</td>
            </tr>
            <tr>
            <td>序號</td>
            <td>4216237DKUSXXQLM /</td>
            </tr>
            </tbody>'''], ['9136625DKITZQIJB','3872753DKKDIVCQE','4216237DKUSXXQLM']),
        (['0206165GDARNOPWX，商品名稱：附贈幻塔虛寶(遊戲虛寶序號一組)'],['0206165GDARNOPWX']),
        (['''<div class="c-article__content">
            <a class="photoswipe-image" href="https://truth.bahamut.com.tw/s01/202308/227aba3be9a6898aa09f1a0c88314194.JPG"><img class="lazyload" data-src="https://truth.bahamut.com.tw/s01/202308/227aba3be9a6898aa09f1a0c88314194.JPG" data-srcset="https://truth.bahamut.com.tw/s01/202308/227aba3be9a6898aa09f1a0c88314194.JPG?w=1000 1x,https://truth.bahamut.com.tw/s01/202308/227aba3be9a6898aa09f1a0c88314194.JPG 2x"/></a><br/>領了說下噢～
            </div>'''],[])
    ]

    for content_elements, expected_result in test_cases:
        assert find_code_in_page(content_elements) == expected_result

def test_multipage_check():
    test_cases = [
        ('''<tr class="b-list__row b-list-item b-imglist-item">
            <td class="b-list__summary">
            <a name="6182"></a>
            <p class="b-list__summary__sort"><a href="B.php?bsn=71040&amp;subbsn=12" data-subbsn="12">影音相關</a></p>
            <span class="b-list__summary__gp b-gp b-gp--normal">1</span>


            </td>
            <td class="b-list__main">
            <a href="C.php?bsn=71040&amp;snA=6182&amp;tnum=1" data-gtm="B頁文章列表-縮圖">
            <div class="b-list__img"><canvas width="120" height="68" data-image="4" data-text="閒聊"></canvas></div>
            <div class="imglist-text">
            <div class="b-list__tile">

            <p data-gtm="B頁文章列表-縮圖" href="C.php?bsn=71040&amp;snA=6182&amp;tnum=1" class="b-list__main__title">【閒聊】幻塔x新世紀福音戰士PV</p>
            </div>
            <p class="b-list__brief">【【幻塔x新世纪福音战士】⚡️沸腾吧DNA⚡️非战斗人员请撤离⚡️A.T立场已展开-哔哩哔哩】https://b23.tv/wlK9Yv0</p>
            </div>
            </a>
            </td>
            <td class="b-list__count">
            <p class="b-list__count__number">
            <span title="互動：3">3</span>/
            <span title="人氣：1,516">1516</span>
            </p>
            <p class="b-list__count__user">
            <a href="https://home.gamer.com.tw/Max6310" target="_blank">Max6310</a>
            </p>
            </td>
            <td class="b-list__time">
            <p class="b-list__time__edittime">
            <a data-gtm="B頁文章列表-縮圖" title="觀看最新回覆文章" href="C.php?bsn=71040&amp;snA=6182&amp;tnum=1&amp;last=1">昨天 10:12</a>
            </p>
            <p class="b-list__time__user">
            <a href="https://home.gamer.com.tw/Max6310" target="_blank">Max6310</a>
            </p>
            </td>
            </tr>''','https://forum.gamer.com.tw/C.php?bsn=71040&snA=6182&tnum=1'),

        ('''<tr class="b-list__row b-list-item b-imglist-item">
            <td class="b-list__summary">
            <a name="786"></a>
            <p class="b-list__summary__sort"><a href="B.php?bsn=71040&amp;subbsn=1" data-subbsn="1">綜合討論</a></p>
            <span class="b-list__summary__gp b-gp b-gp--good">277</span>


            </td>
            <td class="b-list__main">
            <a href="C.php?bsn=71040&amp;snA=786&amp;tnum=95" data-gtm="B頁文章列表-縮圖">
            <div class="b-list__img"><canvas width="120" height="68" data-image="3" data-text="情報"></canvas></div>
            <div class="imglist-text">
            <div class="b-list__tile">

            <p data-gtm="B頁文章列表-縮圖" href="C.php?bsn=71040&amp;snA=786&amp;tnum=95" class="b-list__main__title">【情報】幻塔｜禮包碼序號分享及兌換方式</p><span class="b-list__main__pages"><span class="b-list__page" data-gtm="B頁文章列表-縮圖" data-page="C.php?bsn=71040&amp;snA=786&amp;tnum=95&amp;page=3">3</span><span class="b-list__page" data-gtm="B頁文章列表-縮圖" data-page="C.php?bsn=71040&amp;snA=786&amp;tnum=95&amp;page=4">4</span><span class="b-list__page" data-gtm="B頁文章列表-縮圖" data-page="C.php?bsn=71040&amp;snA=786&amp;tnum=95&amp;page=5">5</span></span>
            </div>
            <p class="b-list__brief">有新的序號我也會第一時間在部落格更新~巴哈也會持續更新 https://minscgame.com/serial-numbe/ 幻塔禮包碼兌換方式幻塔的禮包碼序號兌換方式： 1.解主線任務到畫面右上出現白色禮物箱，…</p>
            </div>
            </a>
            </td>
            <td class="b-list__count">
            <p class="b-list__count__number">
            <span title="互動：114">114</span>/
            <span title="人氣：136,620">136k</span>
            </p>
            <p class="b-list__count__user">
            <a href="https://home.gamer.com.tw/open0416" target="_blank">open0416</a>
            </p>
            </td>
            <td class="b-list__time">
            <p class="b-list__time__edittime">
            <a data-gtm="B頁文章列表-縮圖" title="觀看最新回覆文章" href="C.php?bsn=71040&amp;snA=786&amp;tnum=95&amp;last=1">12-06 09:55</a>
            </p>
            <p class="b-list__time__user">
            <a href="https://home.gamer.com.tw/zaq55662" target="_blank">zaq55662</a>
            </p>
            </td>
            </tr>''','https://forum.gamer.com.tw/C.php?bsn=71040&snA=786&tnum=95&page=5'),

        
        ('''<tr class="b-list__row b-list-item b-imglist-item">
            <td class="b-list__summary">
            <a name="552"></a>
            <p class="b-list__summary__sort"><a href="B.php?bsn=71040&amp;subbsn=1" data-subbsn="1">綜合討論</a></p>
            <span class="b-list__summary__gp b-gp b-gp--best">2377</span>


            </td>
            <td class="b-list__main">
            <a href="C.php?bsn=71040&amp;snA=552&amp;tnum=878" data-gtm="B頁文章列表-縮圖">
            <div class="b-list__img lazyloaded" data-thumbnail="https://truth.bahamut.com.tw/s01/202208/ebf7ef0dbda6c446a2a558d73b45e7c8.JPG?w=300&amp;h=300&amp;fit=o" style="background-image: url(&quot;https://truth.bahamut.com.tw/s01/202208/ebf7ef0dbda6c446a2a558d73b45e7c8.JPG?w=300&amp;h=300&amp;fit=o&quot;);"></div>
            <div class="imglist-text">
            <div class="b-list__tile">

            <p data-gtm="B頁文章列表-縮圖" href="C.php?bsn=71040&amp;snA=552&amp;tnum=878" class="b-list__main__title">【情報】來分享一下女兒吧?</p><span class="b-list__main__pages"><span class="b-list__page" data-gtm="B頁文章列表-縮圖" data-page="C.php?bsn=71040&amp;snA=552&amp;tnum=878&amp;page=42">42</span><span class="b-list__page" data-gtm="B頁文章列表-縮圖" data-page="C.php?bsn=71040&amp;snA=552&amp;tnum=878&amp;page=43">43</span><span class="b-list__page" data-gtm="B頁文章列表-縮圖" data-page="C.php?bsn=71040&amp;snA=552&amp;tnum=878&amp;page=44">44</span></span>
            </div>
            <p class="b-list__brief">8/9日了! 大家準備要賺電費了嗎? 我是說大家要準備開始曬女兒了嗎? 可以色色 全身 剛剛又創了1隻~在115樓</p>
            </div>
            </a>
            </td>
            <td class="b-list__count">
            <p class="b-list__count__number">
            <span title="互動：925">925</span>/
            <span title="人氣：319,752">319k</span>
            </p>
            <p class="b-list__count__user">
            <a href="https://home.gamer.com.tw/kami2021" target="_blank">kami2021</a>
            </p>
            </td>
            <td class="b-list__time">
            <p class="b-list__time__edittime">
            <a data-gtm="B頁文章列表-縮圖" title="觀看最新回覆文章" href="C.php?bsn=71040&amp;snA=552&amp;tnum=878&amp;last=1">昨天 04:08</a>
            </p>
            <p class="b-list__time__user">
            <a href="https://home.gamer.com.tw/priskern" target="_blank">priskern</a>
            </p>
            </td>
            </tr>''','https://forum.gamer.com.tw/C.php?bsn=71040&snA=552&tnum=878&page=44')
    ]

    for html, url in test_cases:
        element = BeautifulSoup(html,'html.parser')
        assert multipage_check(element) == url


if __name__ == "__main__":
    pytest.main()
