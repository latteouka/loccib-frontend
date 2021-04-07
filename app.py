import re

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('48HQs4NCCTIDQpr5eTxYzLUvHkU9w5y/ccCBJm+sgwQpgPNyienG1MG7/FekHh37kmO+aYE027OtOiaQ6t+6u15svu+BguHvpckeD1YrGYBk8d8CHgW4iNAmiAfE6IMqRR8eTjBH7YFj/oqhwvN81QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('020e135fb284c092db4f62a20b585b90')


@app.route("/")
def home():
    return 'server is on!'

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

'''
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    id_search = re.findall(r"id", event.message.text, flags=re.IGNORECASE)

    group_search = re.findall(r"group", event.message.text, flags=re.IGNORECASE)

    if id_search:
        user_id = event.source.user_id
        
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="你的ID是："))
        line_bot_api.push_message(user_id, TextSendMessage(text=user_id))
        
    elif group_search and event.source.group_id:
        group_id = event.source.group_id
        line_bot_api.push_message(group_id, TextSendMessage(text=group_id))
        
    else:
        print("不回應")
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(text="喵"))
'''       


if __name__ == "__main__":
    app.run()

    
