from vars import SLACK_BOT_TOKEN, SLACK_APP_TOKEN
from slack_bolt import Ack, App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=SLACK_BOT_TOKEN)


@app.message("*")
def message_hello(say, message):
    say(f"Hey there <@{message['user']}>!")

@app.command("/orgasm")
def repeat_text(ack, respond, command):
    ack()
    respond(f"thats right: {command['text']}")


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()

