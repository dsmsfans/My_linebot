from pydoc import text
from config import *
import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent
import random

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

import os

# line_bot_api = LineBotApi(dev_lineToken)
line_bot_api = LineBotApi(os.environ['lineToken'])
ua = UserAgent()


def random_proxy():
    ip = ['101.205.120.102', '117.28.246.15']
    return random.choice(ip)


def fetch_picture(event, dump_data):
    num = 0
    stop_crawling = False
    for url_index, i in enumerate(dump_data):
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
                        line_bot_api.push_message(event.source.user_id, ImageSendMessage(
                            original_content_url=pic, preview_image_url=pic))
            if stop_crawling:
                break
    print('Done')


def dcard_crawler(event, board, selected=False):
    try:
        p = requests.Session()
        url = requests.get(f"https://www.dcard.tw/f/{board}",
                           headers={
                               "Referer": "https://www.dcard.tw/",
                               "User-Agent": ua.random
                           },
                           proxies={
                               'http': 'http://' + random_proxy()
                           })
        soup = BeautifulSoup(url.text, "html.parser")
        sel = soup.select("article")
        title = []
        row_data = []
        dump_data = []
        for s in sel:
            row_data.append(s.find('a').get('href'))

        for u in row_data:
            post_data = {
                "before": u[6+len(board)::],
                "limit": "30",
                "popular": "true"
            }
            r = p.get(f"https://www.dcard.tw/_api/forums/{board}/posts", params=post_data, headers={
                "Referer": "https://www.dcard.tw/", "User-Agent": ua.random}, proxies={'http': 'http://' + random_proxy()})
            data2 = json.loads(r.text)
            for u in range(len(data2)):
                Temporary_url = f"/f/{board}/p/" + \
                    str(data2[u]["id"]) + "-" + \
                    str(data2[u]["title"].replace(" ", "-"))
                dump_data.append(Temporary_url)
                title.append(str(data2[u]["title"].replace(" ", "-")))
        if not selected:
            fetch_picture(event, dump_data)
        else:
            return single_selected(event, dump_data, title)
    except Exception as ex:
        print(ex)
        push_text = TextSendMessage(text='請確認是否輸入有誤')
        line_bot_api.push_message(event.source.user_id, push_text)


def single_selected(event, dump_data, title):
    output = []
    column_value = []
    line_bot_api.push_message(event.source.user_id, TextSendMessage(text='Processing! please wait for a second'))
    for url_index, i in enumerate(dump_data):
        if url_index > 30:
            break
        origin_url = "https://www.dcard.tw"+i
        print(f"Page {url_index}'s URL: {origin_url}")
        url = requests.get(origin_url)
        soup = BeautifulSoup(url.text, "html.parser")
        soup.select('picture')
        sel_jpg = soup.find_all('img')
        output.append([])
        num = 0
        for j in sel_jpg:
            if('https' in j['src'] and 'assets' not in j['src'] and 'scorecardresearch' not in j['src']):
                print(f"Picture {url_index}-{num} :", j["src"])
                output[url_index].append(j["src"])
                num += 1
        if output[url_index][0]:
            column_value.append(gen_carousel_template(origin_url, title[url_index], output[url_index][0]), url_index)
        if (url_index % 5) == 0 and url_index > 0:
            carousel_template = TemplateSendMessage(alt_text='Carousel Template', template=CarouselTemplate(columns=column_value[url_index-5:(url_index)]))
            line_bot_api.push_message(event.source.user_id, carousel_template)
    return output


def gen_carousel_template(url, title, picture, idx):
    description = '請選擇'
    select_message = '我要看這個'
    forward_message = '開啟文章'
    column = CarouselColumn(
        thumbnail_image_url=picture,
        title=title,
        text=description,
        actions=[
            PostbackAction(label=select_message, data=f'show_pic({idx})'),
            URITemplateAction(label=forward_message, uri=url)
        ]
    )
    return column


def choose_crawltype(event, board):
    buttons_template = TemplateSendMessage(
        alt_text='Buttons Template',
        template=ButtonsTemplate(
            title='Dcard 爬蟲',
            text='請選擇爬蟲方式',
            actions=[
                MessageTemplateAction(label='我全都要', text='我全都要'),
                MessageTemplateAction(label='我要一個一個選', text='我要一個一個選'),
            ]
        )
    )
    line_bot_api.push_message(event.source.user_id, buttons_template)
    return True
