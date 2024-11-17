from pydantic import BaseModel, Field
from datetime import datetime

class LogEntry(BaseModel):
    uid: int | None = None  # Include the UID for returning existing logs
    source: str = Field(..., title="Log Source", description="Origin of the log, such as a class name")
    log: str = Field(..., title="Log Message", description="The actual log message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, title="Log Timestamp", description="Time the log was created")
