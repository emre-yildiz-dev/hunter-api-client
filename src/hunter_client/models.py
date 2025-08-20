"""Pydantic models for Hunter.io API responses."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl


class EmailSource(BaseModel):
    """Model for email source information."""

    domain: str
    uri: HttpUrl
    extracted_on: str  # API returns date string
    last_seen_on: str  # API returns date string
    still_on_page: bool


class Email(BaseModel):
    """Model for email data."""

    value: EmailStr
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


class DomainSearchMeta(BaseModel):
    """Metadata for domain search results."""

    results: int
    limit: int
    offset: int
    params: Optional[dict[str, str | int]] = None


class DomainSearchResponse(BaseModel):
    """Response model for domain search endpoint."""

    domain: str
    disposable: bool
    webmail: bool
    accept_all: bool
    pattern: Optional[str] = None
    organization: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    twitter: Optional[str] = None
    facebook: Optional[str] = None
    linkedin: Optional[str] = None
    instagram: Optional[str] = None
    youtube: Optional[str] = None
    technologies: list[str] = Field(default_factory=list)
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    street: Optional[str] = None
    emails: list[Email] = Field(default_factory=list)
    meta: Optional[DomainSearchMeta] = None


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


class EmailVerifierResponse(BaseModel):
    """Response model for email verifier endpoint."""

    status: str
    result: str
    score: int
    email: EmailStr
    regexp: bool
    gibberish: bool
    disposable: bool
    webmail: bool
    mx_records: bool
    smtp_server: bool
    smtp_check: bool
    accept_all: bool
    block: bool
    sources: list[EmailSource] = Field(default_factory=list)


class AccountInformationResponse(BaseModel):
    """Response model for account information endpoint."""

    email: EmailStr
    plan_name: str
    plan_level: int
    reset_date: str  # API returns date string
    team_id: Optional[int] = None
    calls: dict[str, dict[str, int]]
