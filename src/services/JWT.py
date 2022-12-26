from datetime import time

import jwt
from fastapi import Request

from core.configs import config


def decodeJWT(token: str) -> dict:
    """Проверка токена на валидность и декодирование"""
    try:
        decoded_token = jwt.decode(token, config.JWT_PUBLIC_KEY)
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return None


async def get_role(request: Request) -> list:
    body = await request.body()
    auth = request.headers.get('Authorization')
    if auth is None:
        return []
    token = auth.split(' ')[1]
    jwt = decodeJWT(token)
    if jwt is None:
        return []
    return jwt['role']
