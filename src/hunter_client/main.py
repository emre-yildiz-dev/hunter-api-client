"""FastAPI application for Hunter.io API client."""

import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

from hunter_client.client import HunterAPIError, HunterClient, create_client
from hunter_client.models import (
    AccountInformationResponse,
    DomainSearchResponse,
    EmailFinderResponse,
    EmailVerifierResponse,
)

load_dotenv()

app = FastAPI(
    title="Hunter.io API Client",
    description="Hunter.io API client with FastAPI",
    version="1.0.0",
)


HTTP_ERROR_CODE = 500
HTTP_BAD_REQUEST = 400
DEFAULT_PORT = 8000
DEFAULT_LIMIT = 10
MAX_LIMIT = 100


def get_client() -> HunterClient:
    """Get Hunter.io client instance."""
    api_key = os.getenv("HUNTER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=HTTP_ERROR_CODE,
            detail="HUNTER_API_KEY environment variable not set",
        )
    return create_client(api_key)


class EmailFinderRequest(BaseModel):
    """Request model for email finder endpoint."""

    domain: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None


class EmailVerifierRequest(BaseModel):
    """Request model for email verifier endpoint."""

    email: EmailStr


@app.get("/", response_model=dict[str, str])
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "Hunter.io API Client",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get("/domain-search", response_model=DomainSearchResponse)
async def domain_search(
    domain: str,
    email_type: Optional[str] = None,
    seniority: Optional[str] = None,
    department: Optional[str] = None,
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
) -> DomainSearchResponse:
    """Search for emails by domain."""
    try:
        with get_client() as client:
            return client.domain_search(
                domain=domain,
                email_type=email_type,
                seniority=seniority,
                department=department,
                limit=limit,
                offset=offset,
            )
    except HTTPException:
        raise
    except HunterAPIError as exc:
        raise HTTPException(
            status_code=exc.status_code or HTTP_ERROR_CODE,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        error_msg = "Internal server error: {0}".format(exc)
        raise HTTPException(
            status_code=HTTP_ERROR_CODE,
            detail=error_msg,
        ) from exc


@app.post("/email-finder", response_model=EmailFinderResponse)
async def email_finder(request: EmailFinderRequest) -> EmailFinderResponse:
    """Find email address."""
    try:
        with get_client() as client:
            return client.email_finder(
                domain=request.domain,
                first_name=request.first_name,
                last_name=request.last_name,
                full_name=request.full_name,
            )
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(
            status_code=HTTP_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except HunterAPIError as exc:
        raise HTTPException(
            status_code=exc.status_code or HTTP_ERROR_CODE,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        error_msg = "Internal server error: {0}".format(exc)
        raise HTTPException(
            status_code=HTTP_ERROR_CODE,
            detail=error_msg,
        ) from exc


@app.post("/email-verifier", response_model=EmailVerifierResponse)
async def email_verifier(request: EmailVerifierRequest) -> EmailVerifierResponse:
    """Verify an email address."""
    try:
        with get_client() as client:
            return client.email_verifier(str(request.email))
    except HTTPException:
        raise
    except HunterAPIError as exc:
        raise HTTPException(
            status_code=exc.status_code or HTTP_ERROR_CODE,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        error_msg = "Internal server error: {0}".format(exc)
        raise HTTPException(
            status_code=HTTP_ERROR_CODE,
            detail=error_msg,
        ) from exc


@app.get("/account", response_model=AccountInformationResponse)
async def account_information() -> AccountInformationResponse:
    """Get account information."""
    try:
        with get_client() as client:
            return client.account_information()
    except HTTPException:
        raise
    except HunterAPIError as exc:
        raise HTTPException(
            status_code=exc.status_code or HTTP_ERROR_CODE,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        error_msg = "Internal server error: {0}".format(exc)
        raise HTTPException(
            status_code=HTTP_ERROR_CODE,
            detail=error_msg,
        ) from exc


@app.exception_handler(HunterAPIError)
async def hunter_api_exception_handler(
    request: object,
    exc: HunterAPIError,
) -> JSONResponse:
    """Handle Hunter API errors."""
    return JSONResponse(
        status_code=exc.status_code or HTTP_ERROR_CODE,
        content={"detail": str(exc)},
    )


def run_server() -> None:
    """Run the FastAPI server."""
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=DEFAULT_PORT)


if __name__ == "__main__":
    run_server()
