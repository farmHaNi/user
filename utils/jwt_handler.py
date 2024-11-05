from time import time
from fastapi import HTTPException, status
from jose import jwt
from utils.setting import Settings

settings = Settings()

# JWT 토큰 생성
def create_jwt_token(user_type: str, user_id: str, id: int) -> str:
    payload = {
        "type": user_type, 
        "user_id": user_id,
        "id": id, 
        "iat": time(), 
        "exp": time() + 3600
    }

    print(settings.SECRET_KEY)

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

# JWT 토큰 검증
def verify_jwt_token(token: str) -> dict:
    print(settings.SECRET_KEY)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if "exp" not in payload or time() > payload["exp"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="다시 로그인해주세요")
        return payload

    except jwt.JWTError as e:
        print(f"JWTError: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="로그인을 해주세요")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="잘못된 접근입니다. 로그인을 해주세요")