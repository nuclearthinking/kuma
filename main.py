from fastapi import FastAPI, Request

from kuma.gitlab import has_reviewers
from kuma.scheme.gitlab_hook import GitlabHook
from kuma.slack import send_slack_mr_notification, SlackMrNotificationData

app = FastAPI()


@app.post("/gitlab/hook")
async def gitlab_hook_handler(request: Request):
    body = await request.json()
    hook_data = GitlabHook(**body)
    if is_new_mr(hook_data):
        await process_new_mr(hook_data)
        return


def is_new_mr(data: GitlabHook) -> bool:
    if data.event_type != "merge_request":
        return False
    return data.object_attributes.action == "open"


async def process_new_mr(data: GitlabHook) -> None:
    if not await has_reviewers(data.object_attributes.iid):
        return
    await send_slack_mr_notification(
        message_data=SlackMrNotificationData(
            name=data.user.name,
            title=data.object_attributes.title,
            url=data.object_attributes.url,
            avatar_url=data.user.avatar_url,
            channel="#web-api-merge_requests",
        )
    )
