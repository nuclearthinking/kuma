from pydantic import BaseModel


class Attributes(BaseModel):
    title: str
    action: str
    iid: int
    url: str


class GitlabUser(BaseModel):
    name: str
    username: str
    id: int
    avatar_url: str


class GitlabHook(BaseModel):
    user: GitlabUser
    event_type: str
    object_attributes: Attributes
