import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class AlertFrequencyEnum(str, Enum):
    daily = "daily"
    weekly = "weekly"
    instant = "instant"


class NotificationTypeEnum(str, Enum):
    JOB_ALERT = "JOB_ALERT"
    APPLICATION_UPDATE = "APPLICATION_UPDATE"
    AI_RECOMMENDATION = "AI_RECOMMENDATION"
    SYSTEM = "SYSTEM"


class JobAlertCreate(BaseModel):
    name: str = Field(..., alias="alert_name")
    query: str
    location: Optional[str] = None
    jobTypes: Optional[List[str]] = None
    remoteOnly: bool = False
    salaryMin: Optional[int] = None
    frequency: AlertFrequencyEnum = AlertFrequencyEnum.daily

    model_config = ConfigDict(populate_by_name=True)


class NotificationResponse(BaseModel):
    id: int
    type: NotificationTypeEnum
    title: str
    message: str
    isRead: bool = Field(alias="is_read")
    createdAt: datetime.datetime = Field(alias="created_at")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
