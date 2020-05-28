from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError
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


carousel_example = TemplateSendMessage(
	alt_text="範例問題",
	template=CarouselTemplate(
		columns=[
			CarouselColumn(
				thumbnail_image_url=url_carousel,
				title="功能介紹 - 實習相關問題",
				text="你可以試著問我這樣的問題",
				actions=[
					MessageTemplateAction(
						label="你有實習的經驗嗎？",
						text="你有實習的經驗嗎？"),
					MessageTemplateAction(
						label="說說你的實習經驗吧",
						text="說說你的實習經驗吧"),
					MessageTemplateAction(
						label="你有相關的工作經驗嗎？",
						text="你有相關的工作經驗嗎？"),]),
			CarouselColumn(
				thumbnail_image_url=url_carousel,
				title="功能介紹 - 學歷相關問題",
				text="你可以試著問我這樣的問題",
				actions=[
					MessageTemplateAction(
						label="你目前就讀那間學校呢？",
						text="你目前就讀那間學校呢？"),
					MessageTemplateAction(
						label="說說你的學歷吧",
						text="說說你的學歷吧"),
					MessageTemplateAction(
						label="你畢業於哪一所學校呢？",
						text="你畢業於哪一所學校呢？"),]),
			CarouselColumn(
				thumbnail_image_url=url_carousel,
				title="功能介紹 - 程式語言相關問題",
				text="你可以試著問我這樣的問題",
				actions=[
					MessageTemplateAction(
						label="你會使用哪些程式語言呢？",
						text="你會使用哪些程式語言呢？"),
					MessageTemplateAction(
						label="說說你會用的語言吧",
						text="說說你會用的語言吧"),
					MessageTemplateAction(
						label="你都用什麼語言寫程式？",
						text="你都用什麼語言寫程式？"),]),
			CarouselColumn(
				thumbnail_image_url=url_carousel,
				title="功能介紹 - 興趣相關問題",
				text="你可以試著問我這樣的問題",
				actions=[
					MessageTemplateAction(
						label="你的興趣是什麼呢？",
						text="你的興趣是什麼呢？"),
					MessageTemplateAction(
						label="說說你的興趣吧",
						text="說說你的興趣吧"),
					MessageTemplateAction(
						label="你有什麼興趣嗎？",
						text="你有什麼興趣嗎？"),]),
			CarouselColumn(
				thumbnail_image_url=url_carousel,
				title="功能介紹 - 履歷相關問題",
				text="你可以試著問我這樣的問題",
				actions=[
					MessageTemplateAction(
						label="可以看看你的履歷嗎？",
						text="可以看看你的履歷嗎？"),
					MessageTemplateAction(
						label="可以提供自傳相關資料嗎？",
						text="可以提供自傳相關資料嗎？"),
					MessageTemplateAction(
						label="有沒有提供簡歷呢？",
						text="有沒有提供簡歷呢？"),])])
)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # print(event)
    """
    * event.message.text 是 使用者傳回來的對話
    * TextSendMessage 則是把傳回來的對話改成可以replay or push 的格式
    * 建議讀者可以自行更改(text=event.message.text) 例如改成 (text="Hello World")
    """
    # profile = line_bot_api.get_profile(event.source.user_id)
    # input_text = event.message.text.encode('utf-8')
    msg = event.message.text
    if ("name" in msg) or ("Hi" in msg) or ("Hello" in msg) or ("你好" in msg) or ("Yo" in msg):
        line_bot_api.push_message(event.source.user_id, StickerSendMessage(package_id=11538, sticker_id=51626494))
        message = TextSendMessage(text="安安你好！\n我是Casper chat bot \n你想知道關於我什麼呢？")
        replay_message(event,message)
    elif ("介紹" in msg) or ("關於我" in msg):
        message = TextSendMessage(text="我叫做范植承\n生日是84/03/18(雙魚座)\n英文名字是Casper\n個性比較悶騷 喜歡嘗試新東西\n好奇心強 熟了話就比較多")
        replay_message(event,message)
    elif ("學歷" in msg) or ("學校" in msg) or ("大學" in msg) or ("研究所" in msg) or ("科系" in msg) or ("學習" in msg):
        message = TextSendMessage(text="我大學畢業於雲林科技大學 資訊工程系\n研究所畢業於臺北科技大學 資訊工程所\n研究方向是資料處理以及演算法")
        replay_message(event,message)
    elif ("經歷" in msg) or ("工作" in msg) or ("實習" in msg) or ("打工" in msg) or ("公司" in msg):
        message = TextSendMessage(text="我的工作經歷\n2014/07~2014/08\n於葛氏兄弟企業有限公司擔任電腦組裝員\n2018/07~2019/10\n於趨勢科擔任Intern")
        replay_message(event,message)
    elif ("程式" in msg) or ("語言" in msg) or ("證照" in msg):
        message = TextSendMessage(text="最擅長的程式語言是python\n其他的語言有C/C++\n大學學過一些Java HTML\n多益成績是850")
        replay_message(event,message)
    elif ("範例" in msg):
        Carousel_template = TemplateSendMessage(
            alt_text='範例問題',
            template=CarouselTemplate(
                columns = [
                    CarouselColumn(
                        thumbnail_image_url='顯示在開頭的大圖片網址',
                        title='this is menu1',
                        text='description1',
                        actions=[
                            PostbackTemplateAction(
                                label='postback1',
                                text='postback text1',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='message1',
                                text='message text1'
                            ),
                            URITemplateAction(
                                label='uri1',
                                uri='http://example.com/1'
                            )
                        ]
                    )
                ]
            )
        )
    else:
        message = TextSendMessage(text=msg)
        replay_message(event,message)
    # if input_text == "name":
    #     message = TextSendMessage(text="My name is Casper")
    #     replay_message(event,message)
 


def replay_message(event,text):
    line_bot_api.reply_message(
        event.reply_token,
        text)
        
def push_message(event,text):
    line_bot_api.push_message(
        event.source.user_id,
        text)        

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