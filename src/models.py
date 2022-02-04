from datetime import datetime
from typing import List

from pydantic import BaseModel


class Foundation(BaseModel):
    id: str
    name: str
    industries: List[str]


class Notification(BaseModel):
    id: str
    timestamp: datetime
    funder: Foundation
    max_opportunity: int
    currency: str


class NotificationResponse(BaseModel):
    notifications: List[Notification]
