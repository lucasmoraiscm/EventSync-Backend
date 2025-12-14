from fastapi import Request, status
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_exact_routes = [
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/auth/login",
            "/auth/register"
        ]

        if request.url.path in public_exact_routes:
            return await call_next(request)
        
        if request.url.path.startswith("/events") and request.method == "GET":
            return await call_next(request)

        if request.url.path.startswith("/users") and request.method == "GET":
            if request.url.path != "/users/me":
                return await call_next(request)
            
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token de autenticação não fornecido"}
            )

        try:
            scheme, token = auth_header.split()

            if scheme.lower() != "bearer":
                raise ValueError("Esquema de autenticação inválido")

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            
            if email is None:
                raise ValueError("Token inválido (sem sub)")

            request.state.user_email = email

        except (JWTError, ValueError) as e:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Credenciais inválidas ou expiradas"}
            )

        return await call_next(request)
