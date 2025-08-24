"""Email finder related models."""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl

from hunter_client.models.common import EmailSource


class EmailFinderRequest(BaseModel):
    """Request model for email finder endpoint."""

    domain: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None


class EmailFinderResponse(BaseModel):
    """Response model for email finder endpoint."""

    email: Optional[EmailStr] = None
    score: Optional[int] = None
    domain: str
    format: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    position: Optional[str] = None
    seniority: Optional[str] = None
    department: Optional[str] = None
    linkedin: Optional[HttpUrl] = None
    twitter: Optional[str] = None
    phone_number: Optional[str] = None
    company: Optional[str] = None
    sources: list[EmailSource] = Field(default_factory=list)
