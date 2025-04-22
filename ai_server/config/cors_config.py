import os

from fastapi.middleware.cors import CORSMiddleware



class CorsConfig:
    @classmethod
    def middlewareConfig(self, app):
        origins = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )