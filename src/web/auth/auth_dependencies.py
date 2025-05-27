from typing import Annotated
from fastapi import WebSocket, Depends, Query, WebSocketException, status
from dependency_injector.wiring import inject, Provide
from application.services.auth_service import AuthService
from core.infrastructure.di.application_container import AplicationContainer
from domain.entities.auth_entities import UserAuth
from src.core.infrastructure.logger.logger import setup_logger

logger = setup_logger('auth.dependencies')

@inject
async def get_websocket_user_session(
    websocket: WebSocket,
    auth_service: Annotated[
        AuthService, Depends(Provide[AplicationContainer.auth_service])
    ],
    token: Annotated[str | None, Query()] = None
) -> UserAuth:
    """
    Autentica una conexión WebSocket.
    Intenta primero con el token de acceso del query parameter.
    Si falla, intenta con el refresh_token de la cookie.

    Retorna:
        user_info: User
    
    Lanza:
        WebSocketException si la autenticación falla.
    """
    user_info: UserAuth | None = None
    logger.info(f"Validando sesión con token: {token}")

    if not token:
        logger.info("No se proporcionó un token de acceso.")
        raise WebSocketException(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Token de autorización requerido o cookie de refresh_token no encontrada."
        )
    
    try:
        logger.info(f"token: {token}")
        user_info = await auth_service.validate_session(token)
    except Exception as e:
        logger.info(f"Error al validar sesión con token: {e}")
        user_info = None

    if not user_info:
        logger.info("No se encontró un usuario válido.")
        refresh_token_cookie = websocket.cookies.get("refresh_token")
        
        if not refresh_token_cookie:
            logger.info("No se encontró un refresh_token en la cookie.")
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Token de autorización requerido o cookie de refresh_token no encontrada."
            )

        try:
            logger.info("Intentando refrescar el token.")
            # Asumimos que refresh_session devuelve un objeto/dict con 'access_token'
            # y opcionalmente 'refresh_token' (y posiblemente datos del usuario).
            # Ajusta esto según lo que realmente devuelva tu servicio.
            new_tokens_obj = await auth_service.refresh_session(refresh_token_cookie)
            
            if not new_tokens_obj or not hasattr(new_tokens_obj, 'access_token'):
                logger.info("Refresh token inválido o fallo al emitir nuevos tokens.")
                raise WebSocketException(
                    code=status.WS_1008_POLICY_VIOLATION,
                    reason="Refresh token inválido o fallo al emitir nuevos tokens."
                )

            # Validar el nuevo access_token inmediatamente
            user_info_after_refresh = await auth_service.validate_session(new_tokens_obj.access_token)
            
            if not user_info_after_refresh:
                logger.info("El token de acceso recién refrescado es inválido.")
                raise WebSocketException(
                    code=status.WS_1008_POLICY_VIOLATION,
                    reason="El token de acceso recién refrescado es inválido."
                )
            
            user_info = user_info_after_refresh

        except WebSocketException: # Re-lanzar si es una excepción que ya controlamos
            raise
        except Exception as e: # Capturar otros errores de auth_service.refresh_session
            # Considera loggear la excepción 'e' para depuración
            print(f"Error durante el refresco del token WebSocket: {e}") # Log simple
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Error durante el proceso de refresco del token."
            )

    return user_info
