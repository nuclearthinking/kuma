import asyncio
import os
from dataclasses import dataclass
from functools import partial

from slack_sdk import WebClient


@dataclass
class SlackMrNotificationData:
    name: str
    title: str
    url: str
    avatar_url: str
    channel: str


def send_slack_message(data: SlackMrNotificationData) -> None:
    client = WebClient(token=os.getenv("SLACK_TOKEN"))
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":grey_exclamation:New merge request.",
                "emoji": True,
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{data.name} opened new merge request <{data.url}|{data.title}>",
            },
        },
        {"type": "divider"},
        {
            "type": "context",
            "elements": [
                {
                    "type": "image",
                    "image_url": data.avatar_url,
                    "alt_text": data.name,
                },
                {"type": "plain_text", "text": data.name, "emoji": True},
            ],
        },
    ]
    client.chat_postMessage(
        channel=data.channel,
        blocks=blocks,
        text=f"{data.name} opened new merge request <{data.title}|{data.url}>",
    )


async def send_slack_mr_notification(message_data: SlackMrNotificationData) -> None:
    loop = asyncio.get_event_loop()
    fnc = partial(send_slack_message, message_data)
    await loop.run_in_executor(executor=None, func=fnc)
