from pydantic import BaseModel


class WatcherResult(BaseModel):

    case_id: str

    action_taken: bool

    action: str

    reason: str