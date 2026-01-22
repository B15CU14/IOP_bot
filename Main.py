import subprocess, os, time
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (Configuration,ApiClient,MessagingApi,MessagingApiBlob,PushMessageRequest,ReplyMessageRequest,
    TextMessage,ImageMessage)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, ImageMessageContent

app = Flask(__name__)
# --- CONFIGURATION ---
CHANNEL_SECRET = '68adbdbc1d8243dc0c0c56449ba48107'
CHANNEL_ACCESS_TOKEN = '0vIy9ECWW1gddmp66e5kwlHY1XhlwSoV5pXS7fHzAnu3iKjqH6mhznO3M/U/jOpbIsGxKp3ru2c937i1Ox4C9KZzy2CTYFDm0ejev9kXQpBpclWL/S+0zgU9K3JazvL/lbrCSpfC55Z+Esu1oK1s8wdB04t89/1O/w1cDnyilFU='
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
TARGET_ID = 'Uf71cb7cdb2dc06017c74e8e6350f0db1'
TARGET_HOSPITAL = 'Hospital A'

# ---------------- Ensure a folder exists to save images-------------------
IMAGE_DIR = './downloaded_images'
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

#---------WEBHOOK ROUTE---------------
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#__________________TEXT RELAY HANDLER__________________
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # 1. Capture the data
    sender_id = event.source.user_id
    incoming_text = event.message.text
    reply_token = event.reply_token

    # 3. Send confirmation reply to sender
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=f'Received, your message is forward to {TARGET_HOSPITAL}')]
            )
        )
    # 4. Push message to destination, test in terminal
    if sender_id != TARGET_ID:
       try:
            line_bot_api.push_message(
                PushMessageRequest(to=TARGET_ID, messages=[TextMessage(text=incoming_text)])
            )
            print(f"✅ SUCCESS: Relayed to {TARGET_ID}")
       except Exception as e:
            print(f"❌ ERROR: Failed to relay. Reason: {e}")


#__________________IMAGE RELAY HANDLER__________________
@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image(event):
    message_id = event.message.id
    reply_token = event.reply_token

    with ApiClient(configuration) as api_client:
        # 1. Use MessagingApiBlob to get the image content
        line_bot_blob_api = MessagingApiBlob(api_client)
        image_content = line_bot_blob_api.get_message_content(message_id)

        # 2. Save the image content to a local file
        file_path = os.path.join(IMAGE_DIR, f"{message_id}.jpg")
        with open(file_path, 'wb') as f:
            f.write(image_content)

        print(f"✅ Image saved to: {file_path}")

        # 3. Reply to the user
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text="Got your photo! I've saved it to my server.")]
            )
        )

#---------------------LOCAL TUNNEL HELPER---------------------------------------
def start_localtunnel(port, subdomain):
    # runs the 'lt' command in the background
    cmd = f"lt --port {port} --subdomain {subdomain}"
    tunnel = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait a moment for it to generate the URL
    time.sleep(2)
    print(f"🚀 Localtunnel started! Check your URL at: https://{subdomain}.loca.lt")
    return tunnel

#----------------MAIN EXECUTION-----------------------
if __name__ == "__main__":
    PORT = 5000
    SUBDOMAIN = 'tired-rat'
    # Start tunnel
    tunnel_process = start_localtunnel(PORT, SUBDOMAIN)
    try:
        # host='0.0.0.0' allows external connections to the port
        app.run(host='0.0.0.0', port=PORT)
    finally:
        tunnel_process.terminate()
        print("\n🛑 Tunnel closed.")