import os
import config
from flask import Flask, abort, request, jsonify
from datetime import datetime
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
from database import (
    db,
    Goal,
    app as app_db
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

secret_key = config.YOUR_CHANNEL_SECRET
access_key = config.YOUR_CHANNEL_ACCESS_TOKEN

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
                        '期限：あなたが目標を達成する期限ex.(2024-12-31)\n'\
                        '------------------\n'\
                        '\n'\
                        'さあ、みんなで頑張ろう！！\n'\

        # メッセージを送信
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
        description = extract_message(text, '目標：')
        deadline = extract_message(text, '期限：')
        today = datetime.today().date()
        today_date = today.strftime('%Y-%m-%d')

        #期限を日付だけ表示
        deadline_date = None
        if deadline:
            try:
                deadline_date = datetime.strptime(deadline, '%Y-%m-%d').date()
                deadline = deadline_date.strftime('%Y-%m-%d')
                print(f"deadline (date): {deadline}")
            except ValueError:
                deadline = None
                print(f"Failed to parse deadline: {deadline}")

        # 抽出結果を確認
        print(f"Extracted name: {name}")
        print(f"Extracted description: {description}")
        print(f"Extracted today: {today_date}")
        print(f"Extracted deadline: {deadline}")

        # データベースに格納するJSONデータを作成
        message_data = {
            'user_id': user_id,
            'name': name,
            'description': description,
            'start': today_date,
            'deadline': deadline
        }
        
        new_goal = Goal(**message_data)
        db.session.add(new_goal)
        db.session.commit()

        # データベースから全ての目標を取得し、出力
        goals = Goal.query.all()
        for goal in goals:
            print(goal)

        # メッセージの内容に基づいてレスポンスを作成
        if name and description and deadline:
            msg = f"名前: {name}\n目標: {description}\n期限: {deadline}"
        else:
            msg =  f'うっわぁ～♥テンプレートあるのに出来ないとかザッコ～♥\n'\
                    '名前、目標、期限を書いてって言ってるのにできないとか恥ずかしくないの～?♥\n'\

        # メッセージを送信
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
    with app_db.app_context():
        db.create_all()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
