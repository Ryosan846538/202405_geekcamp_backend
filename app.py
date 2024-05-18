import os
import config
from flask import Flask, abort, request, jsonify
from datetime import datetime
from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent, JoinEvent, MemberJoinedEvent
from models import init_db
from routes import register_blueprints
from flask_cors import CORS

secret_key = config.YOUR_CHANNEL_SECRET
access_key = config.YOUR_CHANNEL_ACCESS_TOKEN

app = Flask(__name__)
CORS(app)
handler = WebhookHandler(secret_key)
configuration = Configuration(access_token=access_key)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(JoinEvent)
def handle_join(event):
    with ApiClient(configuration) as api_client:
        group_id = event.source.group_id
        print(f"Group ID: {group_id}")
        join_message = f'{group_id} に参加しました'

        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=join_message)]
            )
        )
        group_data = jsonify({'group_id': group_id})

@handler.add(MemberJoinedEvent)
def handle_member_join(event):
    with ApiClient(configuration) as api_client:
        join_message = (
            '参加ありがとう！\n'
            '自分の目標を立ててみんなで達成しよう！！\n'
            '※以下のテンプレートに従って目標を宣言してください\n'
            '------------------\n'
            '名前：自分のなまえ\n'
            '目標：あなたの目標\n'
            '期限：あなたが目標を達成する期限ex.(2024-12-31)\n'
            '------------------\n'
            'さあ、みんなで頑張ろう！！\n'
        )

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
        user_id = event.source.user_id
        print(f"User ID: {user_id}")
        text = event.message.text
        print(f"Received message: {text}")

        name = extract_message(text, '名前：')
        description = extract_message(text, '目標：')
        deadline = extract_message(text, '期限：')
        today = datetime.today().date()
        today_date = today.strftime('%Y-%m-%d')

        deadline_date = None
        try:
            deadline_date = datetime.strptime(deadline, '%Y-%m-%d').date()
            deadline = deadline_date.strftime('%Y-%m-%d')
            print(f"deadline (date): {deadline}")
        except ValueError:
            deadline = None
            print(f"Failed to parse deadline: {deadline}")

        print(f"Extracted name: {name}")
        print(f"Extracted description: {description}")
        print(f"Extracted today: {today_date}")
        print(f"Extracted deadline: {deadline}")

        message_data = {
            'user_id': user_id,
            'name': name,
            'description': description,
            'start': today_date,
            'deadline': deadline
        }
        user_data = jsonify({'user_id': user_id})
        message_json = jsonify(message_data)

        if name and description and deadline:
            msg = f"名前: {name}\n目標: {description}\n期限: {deadline}"
        else:
            msg = (
                'うっわぁ～♥テンプレートあるのに出来ないとかザッコ～♥\n'
                '名前、目標、期限を書いてって言ってるのにできないとか恥ずかしくないの～?♥\n'
            )

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

# Register the blueprints
register_blueprints(app)

if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", 80))
    app.run(host="0.0.0.0", port=port, debug=False)
