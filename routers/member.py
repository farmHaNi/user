from fastapi import APIRouter, Depends, HTTPException, status
from database import get_session
from models.member import Member
from schemas.common import BaseResponse
from schemas.sign import SignUp, SignIn, SignInResponse
from schemas.member import MemberResponse
from utils.authenticate import userAuthenticate
from utils.hash_password import HashPassword
from sqlmodel import select, text
from utils.jwt_handler import create_jwt_token


member_router = APIRouter(
    tags=["사용자"]
)

hash_password = HashPassword()

# 회원가입
@member_router.post("/sign-up", response_model=BaseResponse, status_code=status.HTTP_201_CREATED, summary="사용자 회원가입")
async def sign_new_member(data: SignUp, session = Depends(get_session)) -> BaseResponse:
    # query = text("SELECT * FROM member WHERE user_id = :user_id")
    # session.execute(query, {"user_id": data.user_id})
    # session.commit()
    
    statement = select(Member).where(Member.user_id == data.user_id)
    user = session.exec(statement).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="동일한 사용자가 존재합니다.")
    
    new_member = Member(
        user_id = data.user_id,
        name = data.name,
        password = hash_password.hash_password(data.password),
        email = data.email,
        phone = data.phone,
        type = data.type
    )
    session.add(new_member)
    session.commit()
    return BaseResponse(message = "정상적으로 가입되었습니다.")

# 로그인
@member_router.post("/sign-in", response_model=SignInResponse, status_code=status.HTTP_200_OK, summary="사용자 로그인")
async def sign_in(data: SignIn, session = Depends(get_session))-> SignInResponse:
    statement = select(Member).where(Member.user_id == data.user_id)
    result = session.execute(statement)
    member = result.scalars().first()

    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일치하는 사용자가 존재하지 않습니다.")
    if not hash_password.verify_password(data.password, member.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="패스워드가 일치하지 않습니다.")
    
    delattr(member, "password")
    
    return SignInResponse(
        message = "로그인에 성공했습니다.", 
        user_id = member.user_id, 
        access_token = create_jwt_token(data.type, member.user_id, member.id)
    )

# 정보조회
@member_router.get("/{user_id}", response_model=MemberResponse, status_code=status.HTTP_200_OK, summary="사용자 정보 조회")
async def sign_in(user_id: str, session = Depends(get_session), token_info=Depends(userAuthenticate))-> MemberResponse:
    """
    Authorization 헤더에 토큰을 포함해주세요
    """

    statement = select(Member).where(Member.user_id == user_id)
    result = session.execute(statement)
    member = result.scalars().first()

    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="일치하는 사용자가 존재하지 않습니다.")
    # 토큰의 user_id랑 "/users/{user_id}"의 user_id 비교한 후 다르면 예외처리
    if token_info["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="자기 자신의 정보만 확인 가능합니다.")

    # 실제 유저 정보
    member = Member(
        user_id = member.user_id,
        name = member.name,
        email = member.email,
        phone = member.phone,
        type = member.type
    )


    return MemberResponse(
        message = "유저 조회 완료.",
        user_id=member.user_id,
        name=member.name,
        email=member.email,
        phone=member.phone,
        type=member.type
    )