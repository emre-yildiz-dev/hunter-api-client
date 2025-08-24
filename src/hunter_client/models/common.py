"""Common models used across Hunter.io API."""

from typing import Optional

from pydantic import BaseModel, HttpUrl


class EmailSource(BaseModel):
    """Model for email source information."""

    domain: str
    uri: HttpUrl
    extracted_on: str
    last_seen_on: str
    still_on_page: bool


class Email(BaseModel):
    """Model for email data."""

    email_value: str
    type: str
    confidence: int
    sources: list[EmailSource]
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[str] = None
    seniority: Optional[str] = None
    department: Optional[str] = None
    linkedin: Optional[HttpUrl] = None
    twitter: Optional[str] = None
    phone_number: Optional[str] = None
