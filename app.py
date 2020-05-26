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
        message = TextSendMessage(text="安安你好！\n我是Casper chat bot \n你想知道關於我什麼呢？")
        replay_message(event,message)
    if ("介紹" in msg) or ("關於我" in msg):
        message = TextSendMessage(text="我叫做范植承\n生日是84/03/18(雙魚座)\n英文名字是Casper\n個性比較悶騷 喜歡嘗試新東西\n \
            好奇心強 熟了話就比較多")
        replay_message(event,message)
    if "sex" in msg:
        message = TextSendMessage(text="I'm a boy!")
        replay_message(event,message)
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