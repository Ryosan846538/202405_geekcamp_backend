import os
import config
#import sqlite3
from flask import Flask, abort, request
from linebot.v3.webhook import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    JoinEvent
)

secret_key = config.YOUR_CHANNEL_SECRET
access_key = config.YOUR_CHANNEL_ACCESS_TOKEN

app = Flask(__name__)

handler = WebhookHandler(secret_key)
configuration = Configuration(access_token=access_key)
'''
#データベース接続
def init_db():
    with sqlite3.connect('db_name') as coon:
        conn.cursor()
        conn.commit()
#アプリケーション起動時にデータベースを初期化（たぶんいらない）
init_db()
'''
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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(JoinEvent)
def handle_join(event):
    with ApiClient(configuration) as api_client:
        # グループIDを取得
        group_id = event.source.group_id
        print(f"Group ID: {group_id}")
        '''
        #グループIDをデータベースに保存
        with sqlite3,connect('db_name') as coon:
            c = conn.cursor()
            try:
                c.execute('INSERT INTO groups (group_id) VALUES (?)', (group_id,))
                conn.commit()
            except sqlite3.IntegrityError:
                #すでに存在しているならIDを無視する
                pass
        '''
        # 参加時にメッセージ
        join_message = f'ふつつかものですが、{group_id} に参加させていただきます。'

        # 参加メッセージを送信
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=join_message)]
            )
        )

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        # ユーザーIDを取得
        user_id = event.source.user_id
        print(f"User ID: {user_id}")

        #特定のidの時に条件分岐して返答する
        if user_id == '******':
            print(f"success")
        #相手の送信した内容で条件分岐して回答を変数に代入
            if event.message.text == 'グー':
                msg = 'パー'
            elif event.message.text == 'チョキ':
                msg = 'グー'
            elif event.message.text == 'パー':
                msg = 'チョキ'
            else:
                msg = 'ごめんね。\nまだ他のメッセージには対応してないよ'
        else:
            msg = 'お前は誰だ'

        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=msg)]
            )
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
