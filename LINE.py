from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from linebot.models import VideoSendMessage
import json
import requests
from bs4 import BeautifulSoup
import re
import random
import os
app = Flask(__name__)
LINE_SECRET = os.getenv('LINE_SECRET')
LINE_TOKEN = os.getenv('LINE_TOKEN')
# Channel Access Token
line_bot_api = LineBotApi(LINE_TOKEN)

# Channel Secret
handler = WebhookHandler(LINE_SECRET)

pm_site = {}

reg_imgur_file  =  re.compile('http[s]?://[i.]*imgur.com/\w+')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51'}
url = 'https://www.ptt.cc/bbs/beauty/index.html'
ss = requests.session()
ss.cookies['over18']='1'
images_list = []
for i in range(0,10):
    res = ss.get(url, headers=headers )
    soup = BeautifulSoup(res.text,'html.parser')
    titles = soup.select('div.title a')
    for title in titles:
        restitle = title.text
        # print(restitle)  # 各文章標題
        no_good = ['肉特','大尺碼','以色列','墨西哥','巴西','帥哥']
        if "正妹" in restitle:
            if any(keyword in restitle for keyword in no_good): continue
            # print(restitle)
            resurl = 'https://www.ptt.cc' + title["href"]  # 文章個別網址
            resarticle = ss.get(resurl, headers=headers)  # 利用個別網址再拿取資料
            souparticle = BeautifulSoup(resarticle.text, 'html.parser')  # 利用bs4套件進行解析
            images = reg_imgur_file.findall(resarticle.text)
            for i in images:
                images_list.append(i+".jpg")
    newurl = 'https://www.ptt.cc' + soup.select('a[class="btn wide"]')[1]['href']
    url = newurl

    # 監聽所有來自 /callback 的 Post Request
@app.route("/", methods=['POST'])
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    _token = text.strip().split(" ")
    _low_token = _token[0].lower()
    if text == '飲料':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='喝尿拉')
        )
    elif text == '貼圖':
        line_bot_api.reply_message(
            event.reply_token,
            StickerMessage(
                package_id="1",
                sticker_id="2")
        )
    elif text == '妹子':
        img = random.choice(images_list)
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=img,
                preview_image_url=img)
        )
    elif text == '狗派':
        keyword = 'husky'
        url = "https://imgcdn.cna.com.tw/www/WebPhotos/1024/20190120/077137361902.jpg"
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=url,
                preview_image_url=url)
        )
    elif text == '貓派':
        keyword = 'cat'
        url = "https://img.ltn.com.tw/Upload/liveNews/BigPic/600_phpkXclyo.jpg"
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=url,
                preview_image_url=url)
        )
    elif text == '影片':
        line_bot_api.reply_message(
            event.reply_token,
            VideoSendMessage(
                original_content_url='https://media3.giphy.com/media/3KXKQ41Y0Tqve/giphy.mp4',
                preview_image_url='https://media3.giphy.com/media/3KXKQ41Y0Tqve/giphy.mp4')
        )
    elif text == "地標":
        line_bot_api.reply_message(
            event.reply_token,
            LocationSendMessage(
                title='國立宜蘭大學',
                address='宜蘭縣宜蘭市神農路一段一號',
                latitude=24.746456,
                longitude=121.7466373
            )
        )
    elif text == "樣板":
        buttons_template = TemplateSendMessage(
            alt_text='目錄 template',
            template=ButtonsTemplate(
                title='Template-樣板介紹',
                text='Template分為四種，也就是以下四種：',
                thumbnail_image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png',
                actions=[
                    MessageTemplateAction(
                        label='Buttons Template',
                        text='buttons'
                    ),
                    MessageTemplateAction(
                        label='Confirm template',
                        text='Confirm'
                    ),
                    MessageTemplateAction(
                        label='Carousel template',
                        text='Carousel template'
                    ),
                    MessageTemplateAction(
                        label='Image Carousel',
                        text='Image Carousel'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
    elif text == "buttons":
        btn_template = TemplateSendMessage(
            alt_text='Button Template',
            template=ButtonsTemplate(
                title='按鈕範例標題',
                text='按鈕範例內文',
                thumbnail_image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png',
                actions=[
                    MessageTemplateAction(
                        label='按鈕1',
                        text='按鈕1 內文'
                    ),
                    URITemplateAction(
                        label='按鈕2 URL',
                        uri='https://www.youtube.com/watch?v=2Z2VyaecpGc'
                    ),
                    PostbackTemplateAction(
                        label='按鈕3 POSTBACK',
                        text='postback text',
                        data='postbacks'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, btn_template)
    elif text == "Confirm":
        confirm_template = TemplateSendMessage(
            alt_text='目錄',
            template=ConfirmTemplate(
                text='僅有兩種按鈕用於選擇',
                actions=[
                    PostbackTemplateAction(
                        label='狗派', text='狗派', data='dog'
                    ),
                    MessageTemplateAction(
                        label='貓派', text='貓派'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, confirm_template)
    elif text == "Carousel template":
        Carousel_template = TemplateSendMessage(
            alt_text='目錄',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png',
                        title='Column1',
                        text='Column1',
                        actions=[
                            PostbackTemplateAction(
                                label='postback1',
                                text='postback text1',
                                data='postbacks'
                            ),
                            MessageTemplateAction(
                                label='message1',
                                text='message text1'
                            ),
                            URITemplateAction(
                                label='uri1',
                                uri='https://www.youtube.com/watch?v=2Z2VyaecpGc'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png',
                        title='Column2',
                        text='Column2',
                        actions=[
                            PostbackTemplateAction(
                                label='postback2',
                                text='postback text2',
                                data='postbacks'
                            ),
                            MessageTemplateAction(
                                label='message2',
                                text='message text2'
                            ),
                            URITemplateAction(
                                label='uri2',
                                uri='https://www.youtube.com/watch?v=2Z2VyaecpGc'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png',
                        title='Column3',
                        text='Column3',
                        actions=[
                            PostbackTemplateAction(
                                label='postback3',
                                text='postback text3',
                                data='postbacks'
                            ),
                            MessageTemplateAction(
                                label='message3',
                                text='message text3'
                            ),
                            URITemplateAction(
                                label='uri3',
                                uri='https://www.youtube.com/watch?v=2Z2VyaecpGc'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, Carousel_template)
    elif text == "Image Carousel":
        Image_Carousel = TemplateSendMessage(
            alt_text='Image Carousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png',
                        action=PostbackTemplateAction(
                            label='postback1',
                            text='postback text1',
                            data='postbacks'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://ccsys.niu.edu.tw/exam/img/NIU_mark.png',
                        action=PostbackTemplateAction(
                            label='postback2',
                            text='postback text2',
                            data='postbacks'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, Image_Carousel)


    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )

import os
if __name__ == "__main__":

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)