from pydantic import BaseModel


class DatabaseRow(BaseModel):
    id: int
    text: str
    topic: str
    topic_group: str
    executor: str
    is_processed: bool
