import os
from urllib.parse import urlencode, urlunsplit

import aiohttp


def _get_mr_data_url(review_id: int) -> str:
    path = f"/api/v4/projects/callpanda%2Fweb-api/merge_requests/{review_id}"
    query = urlencode(dict(access_token=os.getenv("GITLAB_TOKEN")))
    return urlunsplit(("https", "gitlab.com", path, query, ""))


async def has_reviewers(mr_id: int) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(_get_mr_data_url(mr_id)) as response:
            json_data = await response.json()
            return bool(json_data.get("reviewers"))
