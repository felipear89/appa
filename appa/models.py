from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Scenario(BaseModel):
    tags: List[str]
    description: str = Field(...)
    payload: dict = Field(...)
    expected: dict = Field(...)
    ignore_fields: Optional[List[str]]


class Feature(BaseModel):
    name: str = Field(...)
    scenarios: List[Scenario]


class ScenarioLog(BaseModel):
    id: str = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
    webhook_messages: Optional[List[dict]]
    returned: Optional[dict]


class TestCommand(BaseModel):
    feature_name: str = Field(...)
