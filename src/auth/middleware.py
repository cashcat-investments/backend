from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from src.containers import AplicationContainer  # Asegúrate que esta importación sea correcta para tu proyecto
from src.auth.service import AuthService  # Para el tipado y la llamada directa al servicio
from src.utils.logger import setup_logger

logger = setup_logger("AuthMiddleware")

# Lista de rutas públicas que no requieren autenticación.
# Deberías ajustar esta lista según las necesidades de tu aplicación.
PUBLIC_PATHS = [
    "/openapi.json",  # Documentación de Swagger UI
    "/docs",          # Documentación de Swagger UI
    "/redoc"          # Documentación de ReDoc
]
# Prefijo para las rutas del servicio de autenticación (login, refresh, etc.)
AUTH_SERVICE_PATHS_PREFIX = "/auth"

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        logger.info(f"Request: {request.url.path}")

        is_public_path = (
           request.url.path in PUBLIC_PATHS or \
           request.url.path.startswith(AUTH_SERVICE_PATHS_PREFIX)  or \
           request.method == "OPTIONS"
        )

        if is_public_path:
            return await call_next(request)

        # Obtiene una instancia de AuthService desde el contenedor de dependencias.
        # Esta forma de obtener el servicio asume que tu contenedor está configurado adecuadamente.
        auth_service_provider = AplicationContainer.auth_package.auth_service
        auth_service: AuthService = auth_service_provider()

        authorization_header: str | None = request.headers.get("Authorization")
        session_info = None  # Almacenará la información de la sesión validada

        if authorization_header is None:
            logger.info("No authorization header")
            return JSONResponse(
                status_code=401,
                content={"detail": "No autenticado: Falta el encabezado de autorización."}
            )
        
        if not authorization_header.startswith("Bearer "):
            logger.info("Invalid authorization header")
            return JSONResponse(
                status_code=401,
                content={"detail": "No autenticado: Encabezado de autorización inválido."}
            )

        token = authorization_header.split("Bearer ")[1]

        if token is None or token == "":
            logger.info("Invalid token")
            return JSONResponse(
                status_code=401,
                content={"detail": "No autenticado: Token inválido."}
            )

        try:
            # validate_session debería devolver datos del usuario/sesión si el token es válido, o None si no lo es.
            session_info = await auth_service.validate_session(token)
        except Exception: # Podrías capturar excepciones más específicas si tu servicio las lanza
            session_info = None # Trata el error como token inválido

        if session_info:
            request.state.current_user = session_info  # Hace la información del usuario accesible en las rutas
            return await call_next(request)
        else:
            # Si el token de acceso es inválido, intenta usar el token de refresco de la cookie.
            refresh_token_cookie: str | None = request.cookies.get("refresh_token")

            if not refresh_token_cookie:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "No autenticado: Falta el encabezado de autorización o la cookie del token de refresco."}
                )

            try:
                # Se asume que refresh_session devuelve un objeto/dict con 'access_token' y 'refresh_token'
                # o None/lanza excepción en caso de fallo.
                new_tokens = await auth_service.refresh_session(refresh_token_cookie)
            except Exception as e:
                # Aquí podrías loggear la excepción 'e' para depuración.
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Fallo al refrescar el token."} # Mensaje genérico por seguridad
                )

            # Verifica que new_tokens no sea None y tenga los atributos esperados.
            # Ajusta hasattr por new_tokens.get("access_token") si es un diccionario.
            if new_tokens and hasattr(new_tokens, 'access_token') and hasattr(new_tokens, 'refresh_token'):
                # Valida el nuevo token de acceso inmediatamente para asegurar que la solicitud actual
                # pueda proceder como autenticada y para poblar request.state.current_user.
                session_info_after_refresh = None
                try:
                    session_info_after_refresh = await auth_service.validate_session(new_tokens.access_token)
                except Exception: # Podrías capturar excepciones más específicas
                    session_info_after_refresh = None

                if session_info_after_refresh:
                    request.state.current_user = session_info_after_refresh
                    response = await call_next(request)

                    # Configura las cookies para los nuevos tokens en la respuesta.
                    # "access_token a una cookie secure=False"
                    # "refresh_token a una cookie secure=True"
                    response.set_cookie(
                        key="access_token",
                        value=new_tokens.access_token,
                        httponly=False,  # Permite que JS lo lea para el header 'Authorization'
                        secure=False,    # Como solicitaste. Para desarrollo. En producción, usualmente True si el sitio es HTTPS.
                        samesite="lax",  # Práctica recomendada
                        path="/"         # Cookie disponible en todo el sitio
                    )
                    response.set_cookie(
                        key="refresh_token",
                        value=new_tokens.refresh_token,
                        httponly=True,   # HttpOnly para seguridad del refresh_token
                        secure=True,     # Como solicitaste. Bueno para producción (HTTPS).
                        samesite="lax",
                        path="/"
                    )
                    return response
                else:
                    # Este caso (token recién refrescado es inválido) idealmente no debería ocurrir.
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Fallo al validar la sesión después de refrescar el token."}
                    )
            else:
                # refresh_session falló o devolvió datos inesperados.
                # Podrías tener un mensaje más específico si tu servicio de refresco devuelve detalles del error.
                response = JSONResponse(
                    status_code=401,
                    content={"detail": "Token de refresco inválido o fallo al emitir nuevos tokens."}
                )

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