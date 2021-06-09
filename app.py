from config import *
import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from crawler import dcard_crawler, choose_crawltype

import os
app = Flask(__name__)

# global variable
echo_flag = False
crawl_enable = False
board = ''
temp_pic = []

# Channel Access Token
# line_bot_api = LineBotApi(dev_lineToken)
line_bot_api = LineBotApi(os.environ['lineToken'])

# Channel Secret
# handler = WebhookHandler(dev_lineSecret)
handler = WebhookHandler(os.environ['lineSecret'])

# 監聽所有來自 /callback 的 Post Request


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global echo_flag, crawl_enable, board, temp_pic
    # print(event)
    """
    * event.message.text 是 使用者傳回來的對話
    * TextSendMessage 則是把傳回來的對話改成可以reply or push 的格式
    * 建議讀者可以自行更改(text=event.message.text) 例如改成 (text="Hello World")
    """

    msg = event.message.text.lower()
    if ("name" in msg) or ("hi" in msg) or ("hello" in msg) or ("你好" in msg) or ("yo" in msg):
        line_bot_api.push_message(
            event.source.user_id,
            StickerSendMessage(package_id=11538, sticker_id=51626494)
        )
        message = TextSendMessage(
            text="安安你好！\n\n我是Casper chat bot \n\n你想知道關於我什麼呢？"
        )
        reply_message(event, message)
    elif ("介紹" in msg) or ("關於我" in msg):
        message = TextSendMessage(
            text="我叫做范植承\n\n生日是84/03/18(雙魚座)\n\n英文名字是Casper\n\n個性比較悶騷 喜歡嘗試新東西\n\n好奇心強 熟了話就比較多\n\n興趣是打排球🏐跟健身🏋🏻")
        reply_message(event, message)
    elif ("學歷" in msg) or ("學校" in msg) or ("大學" in msg) or ("研究所" in msg) or ("科系" in msg) or ("學習" in msg):
        message = TextSendMessage(
            text="大學:\n\n畢業於雲林科技大學\n\n資訊工程系\n\n研究所:\n\n畢業於臺北科技大學\n\n資訊工程所\n\n研究方向及論文:\n\n資料處理以及演算法")
        reply_message(event, message)
    elif ("經歷" in msg) or ("工作" in msg) or ("實習" in msg) or ("打工" in msg) or ("公司" in msg):
        message = TextSendMessage(
            text="我的工作經歷💼\n\nfrom 2014/07 to 2014/08\n\n於葛氏兄弟企業有限公司\n\n擔任電腦組裝員🔧\n\nfrom 2018/07 to 2019/10\n\n於趨勢科擔任Intern")
        reply_message(event, message)
    elif ("程式" in msg) or ("語言" in msg) or ("證照" in msg):
        message = TextSendMessage(
            text="最擅長的程式語言是python\n\n其他的語言有C/C++\n\n大學學過一些Java HTML\n\n多益成績是850")
        reply_message(event, message)
    elif ("範例" in msg):
        choose_crawltype(event)
    elif ("爬蟲" in msg):
        push_text = (
            "歡迎使用爬蟲功能\n \
            請詳閱使用方法\n \
            Ex: dcard (看板 ⚠請輸入英文):\n \
            1.dcard dressup(穿搭版)\n \
            2.dcard food(美食版)\n \
            3.dcard makeup(美妝版)\n \
            4.dcard pet(寵物版)\n.....").replace(' ', '')
        message = TextSendMessage(text=push_text)
        reply_message(event, message)
    elif ("dcard" in msg[0:5]):
        board = msg[5:].replace(' ', '')
        message = TextSendMessage(text=f"即將開始爬{board}版！")
        reply_message(event, message)
        crawl_enable = choose_crawltype(event, board)
    elif ("我全都要" in msg) and crawl_enable:
        dcard_crawler(event, board)
    elif ("我要一個一個選" in msg) and crawl_enable:
        temp_pic = dcard_crawler(event, board, selected=True)
    elif ("測試" in msg):
        carousel_template = TemplateSendMessage(
            alt_text='Carousel Template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg',
                        title='My Facebook',
                        text='description1',
                        actions=[
                            PostbackAction(
                                label='message1',
                                data=123
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/5/58/Instagram-Icon.png',
                        title="My Instagram",
                        text='description1',
                        actions=[
                            URITemplateAction(
                                label="Instagram",
                                uri='https://www.instagram.com/casper_0318/',
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg',
                        title="My Github",
                        text='description1',
                        actions=[
                            URITemplateAction(
                                label="Github",
                                uri='https://github.com/dsmsfans',
                            )
                        ]
                    )
                ]
            )
        )
        reply_message(event, carousel_template)

    elif not echo_flag:
        message = TextSendMessage(text=msg)
        reply_message(event, message)


@handler.add(PostbackEvent)
def handle_postback(event):
    get_parms = event.postback.data
    eval(get_parms, locals=event)


def show_pic(event, idx):
    global temp_pic
    for pic in temp_pic[idx]:
        line_bot_api.push_message(event.source.user_id, ImageSendMessage(
            original_content_url=pic, preview_image_url=pic))


def stop_acho(enable=False):
    global echo_flag
    echo_flag = enable


def reply_message(event, text):
    line_bot_api.reply_message(
        event.reply_token,
        text)


def push_message(event, text):
    line_bot_api.push_message(
        event.source.user_id,
        text)


def fetch_picture(event, a):
    num = 0
    stop_crawling = False
    for url_index, i in enumerate(a):
        if url_index > 1:  # 去除置頂文章
            url = "https://www.dcard.tw"+i
            print(f"Page {url_index}'s URL: {url}")
            url = requests.get(url)
            soup = BeautifulSoup(url.text, "html.parser")
            soup.select('picture')
            sel_jpg = soup.find_all('img')

            for j in sel_jpg:
                if('https' in j['src'] and 'assets' not in j['src'] and 'scorecardresearch' not in j['src']):
                    num += 1
                    if num > 30:
                        stop_crawling = True
                        break
                    else:
                        print(f"Picture {num} :", j["src"])
                        pic = j['src'].replace(".webp", "")
                        push_message(event, ImageSendMessage(
                            original_content_url=pic, preview_image_url=pic))
            if stop_crawling:
                break
    print('Done')


def dcard_crawl(event, board):
    p = requests.Session()
    url = requests.get(f"https://www.dcard.tw/f/{board}")
    soup = BeautifulSoup(url.text, "html.parser")
    sel = soup.select("article")
    a = []
    title = []
    for s in sel:
        a.append(s.find('a').get('href'))
    url = "https://www.dcard.tw/f/" + a[0]

    for k in range(0, 10):
        post_data = {
            "before": a[-1][6 + len(board):15 + len(board)],
            "limit": "30",
            "popular": "true"
        }
        r = p.get(f"https://www.dcard.tw/_api/forums/{board}/posts", params=post_data, headers={
            "Referer": "https://www.dcard.tw/", "User-Agent": "Mozilla/5.0"})
        data2 = json.loads(r.text)
        for u in range(len(data2)):
            Temporary_url = f"/f/{board}/p/" + \
                str(data2[u]["id"]) + "-" + \
                str(data2[u]["title"].replace(" ", "-"))
            a.append(Temporary_url)
    fetch_picture(event, a)


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    # echo sticker
    print(event.message.package_id, event.message.sticker_id)
    try:
        line_bot_api.reply_message(event.reply_token, StickerSendMessage(
            package_id=event.message.package_id, sticker_id=event.message.sticker_id))
    except LineBotApiError:
        line_bot_api.push_message(
            event.source.user_id, TextSendMessage(text='我沒有這個貼圖😭'))
        line_bot_api.push_message(
            event.source.user_id, StickerSendMessage(package_id=2, sticker_id=173))


@app.route('/')
def index():
    return 'I woke up!!'


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
