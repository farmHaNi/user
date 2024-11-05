from pydantic import BaseModel

class SignUp(BaseModel):
    user_id: str
    name: str
    password: str
    email: str
    type: str
    
class SignIn(BaseModel):
    user_id: str
    password: str
    type: str