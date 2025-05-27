from typing import Optional, Dict, Any
import httpx
from fastapi import HTTPException

from core.infrastructure.logger.logger import setup_logger

logger = setup_logger("HTTPClient")

class HTTPClient:
    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        timeout: float = 30.0
    ):
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.timeout = timeout
        self.params = params or {}
        self._client = None
        logger.info("************[Client Started]************")

    async def set_client(self):
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
            params=self.params
        )

    async def _make_request(
        self,
        method: str,
        path: Optional[str] = None,
        params: Optional[Dict[str, str]] = None,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Any:
        if self._client is None:
            await self.set_client()

        async with self._client as client:
            try:
                logger.info(f"************[{method}]************")
                logger.info(f"URL: {self.base_url}{path}" if path else self.base_url)
                logger.info(f"Extra Params: {params}")
                logger.info(f"Body: {body}")
                logger.info(f"Extra Headers: {headers}")
                logger.info(f"Kwargs: {kwargs}")

                response = await client.request(
                    method=method,
                    url=f"{self.base_url}{path}" if path else self.base_url,
                    params=params,
                    json=body,
                    headers=headers,
                    **kwargs
                )
                response.raise_for_status()
                result = response.json()

                logger.info("************[Response]************")
                logger.info(f"{result}")
                logger.info("************[End]************")

                return result
            except httpx.HTTPError as e:
                logger.error("************[Error]************")
                logger.error(f"Error en la llamada a la API: {str(e)}")
                logger.error("************[End]************")
                raise HTTPException(
                    status_code=e.response.status_code if hasattr(e, 'response') else 500,
                    detail=f"Error en la llamada a la API: {str(e)}"
                )
            finally:
                logger.info("************[Client Closed]************")
                await client.aclose()
                self._client = None

    async def get(
        self,
        path: Optional[str] = None,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Any:
        return await self._make_request(
            "GET",
            path,
            params=params,
            headers=headers,
            **kwargs
        )

    async def post(
        self,
        path: Optional[str] = None,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Any:
        return await self._make_request(
            "POST",
            path,
            body=body,
            headers=headers,
            params=params,
            **kwargs
        )

    async def put(
        self,
        path: Optional[str] = None,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Any:
        return await self._make_request(
            "PUT",
            path,
            body=body,
            headers=headers,
            params=params,
            **kwargs
        )

    async def patch(
        self,
        path: Optional[str] = None,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Any:
        return await self._make_request(
            "PATCH",
            path,
            body=body,
            headers=headers,
            params=params,
            **kwargs
        )

    async def delete(
        self,
        path: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Any:
        return await self._make_request(
            "DELETE",
            path,
            headers=headers,
            params=params,
            **kwargs
        )