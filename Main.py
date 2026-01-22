from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    PushMessageRequest,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage
    )
from linebot.v3.webhooks import MessageEvent, TextMessageContent, ImageMessageContent

app = Flask(__name__)

# --- CONFIGURATION ---
CHANNEL_SECRET = '68adbdbc1d8243dc0c0c56449ba48107'
CHANNEL_ACCESS_TOKEN = '0vIy9ECWW1gddmp66e5kwlHY1XhlwSoV5pXS7fHzAnu3iKjqH6mhznO3M/U/jOpbIsGxKp3ru2c937i1Ox4C9KZzy2CTYFDm0ejev9kXQpBpclWL/S+0zgU9K3JazvL/lbrCSpfC55Z+Esu1oK1s8wdB04t89/1O/w1cDnyilFU='
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

#---------PROGRAM---------------
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

#-----------------FUNCTION-----------------------------------------
#__________________TEXT RELAY HANDLER__________________
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # 1. Capture the data
    sender_id = event.source.user_id
    incoming_text = event.message.text
    reply_token = event.reply_token

    # 2. parse the incoming text to get the target ID from database
    SN = incoming_text[0:11]
    #2.1 check if the data format is correct or not


    #2.2 Use SN to send API to database --> return target ID, hospital name
    # getter = database_connector()
    # getter.get_data("API_endpoint", f"{SN}")

    target_id = 'Ue1234'
    hospital_name = 'hospital A'

    #3. test in terminal
    print(f'UserID = {sender_id}'
          f'\nIncoming text = {incoming_text}'
          f'\nTarget ID = {target_id}'
          f'\nHospital = {hospital_name}'
            )

    # 3. Send confirmation reply to sender
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=f'Your message has been forward to {hospital_name}')]
        )
    # 4. Push message to destination, test in terminal
    if sender_id != target_id:
       try:
            line_bot_api.push_message(
                PushMessageRequest(to=target_id, messages=[TextMessage(text=incoming_text)])
            )
            print(f"✅ SUCCESS: Relayed to {target_id}")
        except Exception as e:
            print(f"❌ ERROR: Failed to relay. Reason: {e}")


#__________________IMAGE RELAY HANDLER__________________
@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image(event):
    message_id = event.message.id

    with ApiClient(configuration) as api_client:
        # Use MessagingApiBlob to get the image content
        line_bot_blob_api = MessagingApiBlob(api_client)
        image_content = line_bot_blob_api.get_message_content(message_id)

        # NOTE: To relay an image, you usually need a public URL for the image.
        # If you are just "forwarding," you can't easily pass raw binary data
        # back to LINE's Push API without hosting the image somewhere first.

        print(f"Received image message ID: {message_id}")

        # Simple Notification for the Destination
        line_bot_api = MessagingApi(api_client)
        line_bot_api.push_message(
            PushMessageRequest(
                to=TARGET_USER_ID,
                messages=[TextMessage(text="User sent an image. (Logic for URL hosting required to relay actual file)")]
            )
        )

# 3. The "The URL Catch"
# This is the tricky part: To send an image via ImageMessage, LINE requires a public HTTPS URL for both the original image and a preview thumbnail.
# Because of this, you cannot simply "pipe" the image directly from User A to User B. You usually have two choices:
# The Pro Way: Save the image to a folder on your server (or a service like Imgur/AWS S3) and then send that new URL to the target user.

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)