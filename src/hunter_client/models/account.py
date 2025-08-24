"""Account information related models."""

from typing import Any, Optional

from pydantic import BaseModel, EmailStr


class AccountInformationResponse(BaseModel):
    """Response model for account information endpoint."""

    email: EmailStr
    plan_name: str
    plan_level: int
    reset_date: str
    team_id: Optional[int] = None
    calls: dict[str, Any]
