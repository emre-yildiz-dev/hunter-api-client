"""FastAPI application for Hunter.io API client."""

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from hunter_client.config import (
    DEFAULT_PORT,
    HTTP_BAD_REQUEST,
    HTTP_ERROR_CODE,
)
from hunter_client.dependencies import get_client
from hunter_client.models.account import AccountInformationResponse
from hunter_client.models.domain import DomainSearchParams, DomainSearchResponse
from hunter_client.models.email_finder import (
    EmailFinderRequest,
    EmailFinderResponse,
)
from hunter_client.models.verifier import EmailVerifierRequest, EmailVerifierResponse
from hunter_client.response_handler import HunterAPIError

load_dotenv()

app = FastAPI(
    title='Hunter.io API Client',
    description='Hunter.io API client with FastAPI',
    version='1.0.0',
)


# Module-level variable for dependency injection
domain_search_depends = Depends(DomainSearchParams)


@app.get('/', response_model=dict[str, str])
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        'message': 'Hunter.io API Client',
        'docs': '/docs',
        'openapi': '/openapi.json',
    }


@app.get('/domain-search', response_model=DomainSearchResponse)
async def domain_search(
    search_params: DomainSearchParams = domain_search_depends,
) -> DomainSearchResponse:
    """Search for emails by domain."""
    try:
        with get_client() as client:
            return client.domain.search(
                domain=search_params.domain,
                email_type=search_params.email_type,
                seniority=search_params.seniority,
                department=search_params.department,
                limit=search_params.limit,
                offset=search_params.offset,
            )
    except HunterAPIError as exc:
        raise HTTPException(
            status_code=exc.status_code or HTTP_ERROR_CODE,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        error_msg = 'Internal server error: {0}'.format(exc)
        raise HTTPException(
            status_code=HTTP_ERROR_CODE,
            detail=error_msg,
        ) from exc


@app.post('/email-finder', response_model=EmailFinderResponse)
async def email_finder(request: EmailFinderRequest) -> EmailFinderResponse:
    """Find email address."""
    try:
        with get_client() as client:
            return client.email.find(
                domain=request.domain,
                first_name=request.first_name,
                last_name=request.last_name,
                full_name=request.full_name,
            )
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
        error_msg = 'Internal server error: {0}'.format(exc)
        raise HTTPException(
            status_code=HTTP_ERROR_CODE,
            detail=error_msg,
        ) from exc


@app.post('/email-verifier', response_model=EmailVerifierResponse)
async def email_verifier(request: EmailVerifierRequest) -> EmailVerifierResponse:
    """Verify an email address."""
    try:
        with get_client() as client:
            return client.email.verify(str(request.email))
    except HunterAPIError as exc:
        raise HTTPException(
            status_code=exc.status_code or HTTP_ERROR_CODE,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        error_msg = 'Internal server error: {0}'.format(exc)
        raise HTTPException(
            status_code=HTTP_ERROR_CODE,
            detail=error_msg,
        ) from exc


@app.get('/account', response_model=AccountInformationResponse)
async def account_information() -> AccountInformationResponse:
    """Get account information."""
    try:
        with get_client() as client:
            return client.account.get_information()
    except HunterAPIError as exc:
        raise HTTPException(
            status_code=exc.status_code or HTTP_ERROR_CODE,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        error_msg = 'Internal server error: {0}'.format(exc)
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
        content={'detail': str(exc)},
    )


def run_server() -> None:
    """Run the FastAPI server."""
    uvicorn.run(app, host='127.0.0.1', port=DEFAULT_PORT)


if __name__ == '__main__':
    run_server()
