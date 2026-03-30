from cash_control.domain.interfaces.user_repository import UserRepository
from cash_control.application.dtos.auth_dto import LoginDTO
from cash_control.core.security import verify_password, create_access_token


class LoginUserUseCase:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def execute(self, dto: LoginDTO):

        user = self.repo.get_by_email(dto.email)

        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(dto.password, user.hashed_password):
            raise ValueError("Invalid credentials")

        token = create_access_token({
            "sub": user.email
        })

        return token