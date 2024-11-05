from pydantic import BaseModel, Field, EmailStr
from enums.member_type import MemberType
from models.member import Member
from schemas.common import BaseResponse

class SignUp(BaseModel):
    user_id: str = Field(unique=True, description="사용자 아이디")
    name: str = Field(description="사용자 이름")
    password: str = Field(description="사용자 패스워드")
    email: EmailStr = Field(description="사용자 이메일")
    type: MemberType = Field(description="사용자 타입")
    
class SignIn(BaseModel):
    user_id: str = Field(description="사용자 아이디")
    password: str = Field(description="사용자 패스워드")
    type: MemberType = Field(description="사용자 타입")

class SignInResponse(BaseResponse):
    user: str = Field(description="유저 아이디")
    access_token: str = Field(description="엑세스 토큰")
