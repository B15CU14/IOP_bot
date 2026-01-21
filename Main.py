from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)

# --- CONFIGURATION ---
# Get these from https://developers.line.biz/
CHANNEL_SECRET = '68adbdbc1d8243dc0c0c56449ba48107'
CHANNEL_ACCESS_TOKEN = '0vIy9ECWW1gddmp66e5kwlHY1XhlwSoV5pXS7fHzAnu3iKjqH6mhznO3M/U/jOpbIsGxKp3ru2c937i1Ox4C9KZzy2CTYFDm0ejev9kXQpBpclWL/S+0zgU9K3JazvL/lbrCSpfC55Z+Esu1oK1s8wdB04t89/1O/w1cDnyilFU='

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# This function handles Text Messages
# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         user_input = event.message.text
#         # Replays the exact same text the user sent
#         line_bot_api.reply_message_with_http_info(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=event.message.text)]
#             )
#         )

# Function to check if input is number
@handler.add(MessageEvent, message=TextMessageContent)
def if_num (event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        user_input = event.message.text
        answer = print(user_input.isdigit())
        user_input.isdigit()
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=answer)]
            )
        )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)