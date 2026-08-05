from pydantic import BaseModel

from memory.timeline import TimelineEvent


class CaseHistory(BaseModel):

    events: list[TimelineEvent] = []