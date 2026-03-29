from cash_control.domain.interfaces.user_repository import UserRepository
from cash_control.application.dtos.user_dto import CreateUserDTO
from cash_control.core.security import hash_password
from cash_control.domain.entities.user import User

class CreateUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    def execute(self, dto: CreateUserDTO):
        user = User(
            name=dto.name,
            email=dto.email,
            hashed_password=hash_password(dto.password)
        )
        return self.repo.create(user)