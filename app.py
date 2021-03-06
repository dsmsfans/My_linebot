import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *
import os
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.environ['lineToken'])
# Channel Secret
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
    # print(event)
    """
    * event.message.text 是 使用者傳回來的對話
    * TextSendMessage 則是把傳回來的對話改成可以reply or push 的格式
    * 建議讀者可以自行更改(text=event.message.text) 例如改成 (text="Hello World")
    """
    # profile = line_bot_api.get_profile(event.source.user_id)
    # input_text = event.message.text.encode('utf-8')
    msg = event.message.text.lower()
    if ("name" in msg) or ("hi" in msg) or ("hello" in msg) or ("你好" in msg) or ("yo" in msg):
        line_bot_api.push_message(event.source.user_id, StickerSendMessage(
            package_id=11538, sticker_id=51626494))
        message = TextSendMessage(
            text="安安你好！\n\n我是Casper chat bot \n\n你想知道關於我什麼呢？")
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
        buttons_template = TemplateSendMessage(
            alt_text='Buttons Template',
            template=ButtonsTemplate(
                title='這是範例問題',
                text='選擇下列按鈕可以認識我',
                thumbnail_image_url='https://vignette.wikia.nocookie.net/spongebobsquarepants/images/7/7f/Patrick_Star-1-.svg/revision/latest/top-crop/width/360/height/450?cb=20140617123710&path-prefix=zh',
                actions=[
                    MessageTemplateAction(label='學歷', text='學歷',),
                    MessageTemplateAction(label='經歷', text='經歷'),
                    MessageTemplateAction(label='介紹', text='介紹')
                ]
            )
        )
        reply_message(event, buttons_template)

    elif ("爬蟲" in msg):
        message = TextSendMessage(
            text="可輸入dcard後接看板\n\nEx:dcard dressup\n\n範例看板:\n\n1.dressup(穿搭版)\n\n2.food(美食版)\n\n3.makeup(美妝版)\n\n4.pet(寵物版)\n\n.....")
        reply_message(event, message)

    elif ("dcard" in msg[0:5]):
        message = TextSendMessage(text=f"開始爬{msg[5:]}版！🥳")
        reply_message(event, message)
        dcard_crawl(event, msg[5:])

    elif ("測試" in msg):
        carousel_template = TemplateSendMessage(
            alt_text='Carousel Template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg',
                        title='My Facebook',
                        actions=[
                            URITemplateAction(
                                label='Facebook',
                                uri='https://www.facebook.com/profile.php?id=100001440018890',
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/5/58/Instagram-Icon.png',
                        title="My Instagram",
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

    else:
        message = TextSendMessage(text=msg)
        reply_message(event, message)


def reply_message(event, text):
    line_bot_api.reply_message(
        event.reply_token,
        text)


def push_message(event, text):
    line_bot_api.push_message(
        event.source.user_id,
        text)


def dcard_crawl(event, b):
    board = b.replace(" ","")
    print(board)
    p = requests.Session()
    url = requests.get(f"https://www.dcard.tw/f/{board}")
    soup = BeautifulSoup(url.text, "html.parser")
    sel = soup.select("div.sc-1azsmde-0")
    a = []
    for s in sel:
        a.append(s.find('a').get('href'))
    url = "https://www.dcard.tw" + a[0]
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
    num = 0

    for url_index, i in enumerate(a):
        url = "https://www.dcard.tw"+i
        print(f"Page {url_index}'s URL: {url}")
        url = requests.get(url)
        soup = BeautifulSoup(url.text, "html.parser")
        sel_jpg = soup.find_all('img')
        for j in sel_jpg:
            if('https' in j['src']) and num < 20:
                num += 1
                # print(f"Picture {num} :", j["src"])
                pic = j['src']
                if pic[-4:] == 'webp' or pic[-3:] == 'jpg':
                    pic = pic.replace('webp','jpeg')
                    push_message(event,ImageSendMessage(original_content_url=pic,preview_image_url=pic))
                else:
                    break


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
