from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from src.presentation.middlewares.logging import logging_middleware
from src.presentation.middlewares.auth import AuthMiddleware


def setup_global_middlewares(app: FastAPI):
    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["localhost", "127.0.0.1", "example.com"]
    )

    app.add_middleware(AuthMiddleware)

    app.middleware("http")(logging_middleware)
