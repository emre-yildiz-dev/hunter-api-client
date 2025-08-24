"""Email verifier related models."""

from pydantic import BaseModel, EmailStr, Field

from hunter_client.models.common import EmailSource


class EmailVerifierRequest(BaseModel):
    """Request model for email verifier endpoint."""

    email: EmailStr


class EmailVerifierResponse(BaseModel):
    """Response model for email verifier endpoint."""

    status: str
    verification_result: str = Field(alias='result')
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
