from sys import argv
from vars import SLACK_BOT_TOKEN
from slack_sdk import WebClient


# link = "http://i.ytimg.com/vi/toz71XAofPc/hqdefault.jpg"
link = argv[1:][0]

thing = WebClient(token=SLACK_BOT_TOKEN)

thing.chat_postMessage(
    channel="general",
    text="Rydd opp rotet!",
    attachments=[
            {
                "fallback": "rot",
                "image_url": link
            }]
)
