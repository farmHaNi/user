from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_session
from app.models.user import Users
from app.schemas.sign import SignUp
from app.utils.authenticate import userAuthenticate
from app.utils.hash_password import HashPassword
from sqlmodel import select, text
from app.utils.jwt_handler import create_jwt_token


user_router = APIRouter(
    tags=["User"]
)

hash_password = HashPassword()

# 회원가입
@user_router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def sign_new_employee(data: SignUp, session = Depends(get_session)) -> dict:
    # query = text("SELECT * FROM users WHERE user_id = :user_id")
    # session.execute(query, {"user_id": data.user_id})
    # session.commit()
    
    statement = select(Users).where(Users.user_id == data.user_id)
    user = session.exec(statement).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="동일한 사용자가 존재합니다.")
    
    new_user = Users(
        user_id = data.user_id,
        name = data.name,
        password = hash_password.hash_password(data.password),
        email = data.email,
        type = data.type
    )
    session.add(new_user)
    session.commit()
    return {"message": "정상적으로 가입되었습니다."}

# 로그인
@user_router.post("/sign-in")
async def sign_in(data: Users, session = Depends(get_session))-> dict:
    statement = select(Users).where(Users.user_id == data.user_id)
    result = session.execute(statement)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일치하는 사용자가 존재하지 않습니다.")
    if not hash_password.verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="패스워드가 일치하지 않습니다.")
    
    return {
        "message": "로그인에 성공했습니다.", 
        "user": list(user), 
        "access_token": create_jwt_token(data.type, user.user_id, user.id)
        }

# 정보조회
@user_router.get("/{user_id}")
async def sign_in(user_id: str, session = Depends(get_session), token_info=Depends(userAuthenticate))-> dict:
    statement = select(Users).where(Users.user_id == user_id)
    result = session.execute(statement)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일치하는 사용자가 존재하지 않습니다.")
    # 토큰의 user_id랑 "/users/{user_id}"의 user_id 비교한 후 다르면 예외처리
    if token_info["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="자기 자신의 정보만 확인 가능합니다.")

    # 실제 유저 정보
    user = Users(
        user_id = user.user_id,
        name = user.name,
        email = user.email,
        type = user.type
    )

    return {
        "message": "유저 조회 완료.", 
        "user": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "type": user.type
        } 
    }