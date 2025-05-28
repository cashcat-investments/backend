from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from dependency_injector.wiring import Provide, inject

from src.application.services.auth_service import AuthService
from src.infrastructure.config.application_container import AplicationContainer
from src.application.dtos.auth_dtos import SignUpRequest
from src.web.auth.auth_constants import AUTH_PREFIX
from src.domain.entities.auth_entities import CredentialsEntity, OAuthResponseEntity, TokensEntity
from src.domain.entities.user_entities import UserProfileEntity

router = APIRouter(prefix=f'/{AUTH_PREFIX}', tags=[AUTH_PREFIX])

@router.post("/login/local", response_model=UserProfileEntity)
@inject
async def login(
    body: CredentialsEntity,
    service: Annotated[
        AuthService,
        Depends(Provide[AplicationContainer.auth_service])
    ]
):
    login_data = await service.login_local(body)

    if login_data is None:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    response = JSONResponse(content=login_data.user.model_dump())
    return _set_cookies(response, login_data.tokens)


@router.post("/register/local", response_model=UserProfileEntity)
@inject
async def register(
    body: SignUpRequest,
    service: Annotated[
        AuthService,
        Depends(Provide[AplicationContainer.auth_service])
    ]
):
    register_data = await service.register_local(body)

    if register_data is None:
        raise HTTPException(status_code=400, detail="User already exists")

    response = JSONResponse(content=register_data.user.model_dump())
    return _set_cookies(response, register_data.tokens)


@router.post("/sign-in/google", response_model=OAuthResponseEntity)
@inject
async def google_redirect(
    redirect_to: str,
    service: Annotated[
        AuthService,
        Depends(Provide[AplicationContainer.auth_service])
    ]
):
    response = await service.sign_in_with_google(redirect_to)
    if response is None:
        raise HTTPException(status_code=500, detail="Failed to sign in with Google")
    return response


@router.post("/sign-in/google/validate-code", response_model=UserProfileEntity)
@inject
async def validate_google_code(
    code: str,
    service: Annotated[
        AuthService,
        Depends(Provide[AplicationContainer.auth_service])
    ]
):
    sign_in_data = await service.validate_code(code)

    if sign_in_data is None:
        raise HTTPException(status_code=400, detail="Invalid Google code")
    
    response = JSONResponse(content=sign_in_data.user.model_dump())
    return _set_cookies(response, sign_in_data.tokens)


@router.post("/sign-out")
async def sign_out():
    response = JSONResponse(content={"detail": "Logged out successfully"})
    return _clear_cookies(response)


def _set_cookies(response: JSONResponse, tokens: TokensEntity):
    response.set_cookie(key="access_token", value=tokens.access_token, httponly=False)
    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True)
    return response

def _clear_cookies(response: JSONResponse):
    response.set_cookie(
        key="access_token",
        value='',
        httponly=False,
        secure=False,
        samesite="lax",
        path="/",
        max_age=0
    )
    response.set_cookie(
        key="refresh_token",
        value='',
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
        max_age=0
    )
    return response