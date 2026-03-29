from pydantic import BaseModel, EmailStr

class CreateUserDTO(BaseModel):
    name: str
    email:EmailStr
    password: str
    
class UserResponseDTO(BaseModel):
    id: int
    name: str
    email: EmailStr