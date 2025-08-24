"""Domain search related models."""

from typing import Optional

from pydantic import BaseModel, Field

from hunter_client.models.common import Email


class DomainSearchParams(BaseModel):
    """Query parameters for domain search."""

    domain: str
    email_type: Optional[str] = None
    seniority: Optional[str] = None
    department: Optional[str] = None
    limit: int = 10
    offset: int = 0


class DomainSearchMeta(BaseModel):
    """Metadata for domain search results."""

    total_results: int
    limit: int
    offset: int
    search_params: Optional[dict[str, str | int]] = None


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
