import os
from dotenv import load_dotenv
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy


load_dotenv()


# Setings Authentication backends
SECRET_KEY_BY_JWT = os.environ.get('SECRET_KEY_BY_JWT')
SECRET_KEY_BY_UserManager = os.environ.get('SECRET_KEY_BY_UserManager')

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY_BY_JWT, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
