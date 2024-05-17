import os
import config
import json
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
    JoinEvent,
    MemberJoinedEvent
)

secret_key = config.YOUR_CHANNEL_SECRET
access_key = config.YOUR_CHANNEL_ACCESS_TOKEN

app = Flask(__name__)

handler = WebhookHandler(secret_key)
configuration = Configuration(access_token=access_key)

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
        #json形式に変換
        group_data = json.dumps({'group_id': group_id})
        # 参加時にメッセージ
        join_message = f'{group_id} に参加しました'

        # 参加メッセージを送信
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=join_message)]
            )
        )

@handler.add(MemberJoinedEvent)
def handle_member_join(event):
    with ApiClient(configuration) as api_client:
        # 参加した人にメッセージ送信
        join_message = f'参加ありがとう！\n'\
                        '自分の目標を立ててみんなで達成しよう！！\n'\
                        '※以下のテンプレートに従って目標を宣言してください\n'\
                        '------------------\n'\
                        '名前：自分のなまえ\n'\
                        '目標：あなたの目標\n'\
                        '説明：あなたが達成したい目標の説明\n'\
                        '期限：あなたが目標を達成する期限\n'\
                        '------------------\n'\
                        '\n'\
                        'さあ、みんなで頑張ろう！！\n'\

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
        #メッセージテキストを取得
        text = event.message.text
        print(f"Received message: {text}")

        # 各フィールドを抽出
        name = extract_message(text, '名前：')
        goal = extract_message(text, '目標：')
        description = extract_message(text, '説明：')
        deadline = extract_message(text, '期限：')

        # 抽出結果を確認
        print(f"Extracted name: {name}")
        print(f"Extracted goal: {goal}")
        print(f"Extracted description: {description}")
        print(f"Extracted deadline: {deadline}")

        # データベースに格納するJSONデータを作成
        message_data = {
            'user_id': user_id,
            'name': name,
            'goal': goal,
            'description': description,
            'deadline': deadline
        }
        message_json = json.dumps(message_data)

        # メッセージの内容に基づいてレスポンスを作成
        if name and goal and description and deadline:
            msg = f"名前: {name}\n目標: {goal}\n説明: {description}\n期限: {deadline}"
        else:
            msg = 'うっわぁ～♥テンプレートあるのに出来ないとかザッコ～♥\n名前、目標、説明、期限を書いてって言ってるのにできないとか恥ずかしくないの～?♥\n'
        '''
        #「名前：」というメッセージが存在しているかチェック
        if '名前：' in text:
            # 「名前：」の次に続く文字列を抽出
            try:
                name = text.split('名前：')[1].strip()
                print(f"Extracted name: {name}")
                msg = f"名前を取得しました：{name}"
            except IndexError:
                msg = '名前が指定されたメッセージの次の行が見つかりませんでした。'
        else:
            msg = 'そんなこと言わないで目標に向かって頑張ろう！！'
        '''
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=msg)]
            )
        )

def extract_message(text, field_name):
    try:
        return text.split(field_name)[1].split('\n')[0].strip()
    except IndexError:
        return None


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
