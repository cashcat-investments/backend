from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.containers import AplicationContainer
from src.auth.service import AuthService
from src.auth.models import AUTH_PREFIX, LocalLoginRequest, User, LocalRegisterRequest
from dependency_injector.wiring import Provide, inject


router = APIRouter(prefix=f'/{AUTH_PREFIX}', tags=[AUTH_PREFIX])

@router.post("/login/local", response_model=User)
@inject
async def login(
    body: LocalLoginRequest,
    auth_service: Annotated[
        AuthService,
        Depends(Provide[AplicationContainer.auth_package.auth_service])
    ]
):
    login_data = await auth_service.login(body)

    if login_data is None:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    response = JSONResponse(content=login_data.user.model_dump())
    response.set_cookie(key="access_token", value=login_data.access_token, httponly=False)
    response.set_cookie(key="refresh_token", value=login_data.refresh_token, httponly=True)

    return response


@router.post("/register/local", response_model=User)
@inject
async def register(
    body: LocalRegisterRequest,
    auth_service: Annotated[
        AuthService,
        Depends(Provide[AplicationContainer.auth_package.auth_service])
    ]
):
    register_data = await auth_service.register(body)

    if register_data is None:
        raise HTTPException(status_code=400, detail="User already exists")

    response = JSONResponse(content=register_data.user.model_dump())
    response.set_cookie(key="access_token", value=register_data.access_token, httponly=False)
    response.set_cookie(key="refresh_token", value=register_data.refresh_token, httponly=True)

    return response


@router.post("/sign-in/google")
@inject
async def google_redirect(
    redirect_to: str,
    auth_service: Annotated[
        AuthService,
        Depends(Provide[AplicationContainer.auth_package.auth_service])
    ]
):
    response = await auth_service.sign_in_with_google(redirect_to)
    if response is None:
        raise HTTPException(status_code=500, detail="Failed to sign in with Google")
    return response


@router.post("/sign-in/google/validate-code")
@inject
async def validate_google_code(
    code: str,
    auth_service: Annotated[
        AuthService,
        Depends(Provide[AplicationContainer.auth_package.auth_service])
    ]
):
    sign_in_data = await auth_service.validate_google_code(code)

    if sign_in_data is None:
        raise HTTPException(status_code=400, detail="Invalid Google code")
    
    response = JSONResponse(content=sign_in_data.user.model_dump())
    response.set_cookie(key="access_token", value=sign_in_data.access_token, httponly=False)
    response.set_cookie(key="refresh_token", value=sign_in_data.refresh_token, httponly=True)

    return response


@router.post("/sign-out")
async def sign_out():
    response = JSONResponse(content={"detail": "Logged out successfully"})
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