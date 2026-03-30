from cash_control.domain.interfaces.user_repository import UserRepository
from cash_control.application.dtos.user_dto import CreateUserDTO
from cash_control.core.security import hash_password
from cash_control.domain.entities.user import User

class CreateUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    def execute(self, dto: CreateUserDTO):
        existing_user = self.repo.get_by_email(dto.email)        
        
        if existing_user:
            raise ValueError("Email já utilizado, escolha outro.")
        
        hashed_password = hash_password(dto.password)
        
        user = User(
            name=dto.name,
            email=dto.email,
            hashed_password=hash_password(dto.password)
        )

        return self.repo.create(user)