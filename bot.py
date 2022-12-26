from model import sheet
from datetime import datetime
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    StickerMessage, StickerSendMessage,
    ConfirmTemplate, TemplateSendMessage,
    MessageAction, URIAction, LocationMessage,
)

gs = sheet.GoogleSheet('我的試算表','推薦')

line_bot_api = LineBotApi('G6csKv5mME3+kYXVQgsjz5AwF7jldMVsQ38EBYCrlzFixNM9/9dzrepiyS+GbIXW0FvkurE1EZcXDIDABAUdlyICLeokokQzvVt9KXl8U8cIxqvjGbgFqayGICokk+riOPgC972ROemMwhgFgKZK2wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d98e15b1c5b83da099b7475c55ed1199')

users = {}

def check_user(id, name):
    global users

    if id not in users:
        users[id] = {
            'name':name,
            'logs':{'日期時間':'', '經緯度':'', '地址':'', '說明':''},
            'save':False 
        }

app = Flask(__name__)

def reply_text(token, id, txt):
    global users
    me = users[id]

    if me['save']  == False:
        if '推薦' in txt:
            queries = ConfirmTemplate(
                text=f"{me['name']}您好，請問有好地方要推薦我嗎？", 
                actions=[
                    URIAction(
                        label='有！地點在...',
                        uri='line://nv/location'
                    ),
                    MessageAction(label='沒有耶', text='沒有耶')
                ])

            temp_msg = TemplateSendMessage(alt_text='確認訊息',
                                        template=queries)
            line_bot_api.reply_message(token, temp_msg)
            me['save'] = True # 開始紀錄訊息

            temp_msg = TemplateSendMessage(alt_text='確認訊息',
                                        template=queries)
            line_bot_api.reply_message(token, temp_msg)
            me['save'] = True # 開始紀錄訊息

        else:
            line_bot_api.reply_message(
                token,
                TextSendMessage(text="收到訊息了，謝謝！"))
    else:
        if txt=='沒有耶':
            line_bot_api.reply_message(
                token,
                TextSendMessage(text="好的，有想到再來推薦我~"))
        elif me['logs']['說明'] == '':
            line_bot_api.reply_message(
                token,
                TextSendMessage(text="我記下來了，超級感謝您！"))
            me['logs']['說明'] = txt  # 儲存說明
            # 日期要設置成台北時間
            dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            me['logs']['日期時間'] = dt
            me['save'] = False   # 紀錄完畢

            print('資料紀錄:', me['logs'])
            logs = [id, me['name'], me['logs']['日期時間'], 
                        me['logs']['經緯度'], me['logs']['地址'], me['logs']['說明']]
            gs.append_row(logs)

@app.route('/')
def index():
    return 'Welcome to Line Bot!'

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.default()
def default(event):
    print('捕捉到事件：', event)

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    _id = event.source.user_id
    profile = line_bot_api.get_profile(_id)
    # 紀錄用戶資料
    _name = profile.display_name
    print('大頭貼網址：', profile.picture_url)
    print('狀態消息：', profile.status_message)
    check_user(_id, _name)

    txt=event.message.text

    reply_text(event.reply_token, _id, txt)

# 處理地點訊息
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    global users

    _id = event.source.user_id
    me = users[_id]
    addr=event.message.address    # 地址
    lat=str(event.message.latitude)    # 緯度
    lon=str(event.message.longitude)   # 經度

    if addr is None:
        msg=f'收到GPS座標：({lat}, {lon})\n謝謝您！'
    else:
        msg=f'收到GPS座標：({lat}, {lon})。\n地址：{addr}\n謝謝您！'

    if  me['save']:
        me['logs']['經緯度'] = f'({lat}, {lon})'
        me['logs']['地址'] = addr

        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=msg),
                TextSendMessage(text='方便說明這是什麼地方嗎？')
        ])
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
    # app.run()