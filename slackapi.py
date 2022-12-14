from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging

# Local
from vars import SLACK_BOT_TOKEN
from random_messages import custom_message


def send_message(chat: str, message: str) -> None:
    thing = WebClient(token=SLACK_BOT_TOKEN)

    thing.chat_postMessage(
        channel=chat,
        text=custom_message(message),
        # attachments=[
        #         {
        #             "fallback": "rot",
        #             "image_url": link
        #         }]
    )


# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
def upload(image_URI, message, channel_id, log_state=True):
    client = WebClient(SLACK_BOT_TOKEN)
    logger = logging.getLogger(__name__)

    try:
        # Call the files.upload method using the WebClient
        # Uploading files requires the `files:write` scope
        result = client.files_upload(
            channels=channel_id, initial_comment=custom_message(message), file=image_URI
        )
        # Log the result
        if log_state:
            logger.info(result)

    except SlackApiError as e:
        logger.error("Error uploading file: {}".format(e))
