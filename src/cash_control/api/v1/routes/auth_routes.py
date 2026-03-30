from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from cash_control.core.database import SessionLocal
from cash_control.infrasctructure.repositories.user_repository_impl import UserRepositoryImpl
from cash_control.application.use_cases.login_user import LoginUserUseCase
from cash_control.application.dtos.auth_dto import LoginDTO, TokenResponseDTO

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository(db: Session = Depends(get_db)):
    return UserRepositoryImpl(db)


@router.post("/login", response_model=TokenResponseDTO)
def login(
    dto: LoginDTO,
    repo: UserRepositoryImpl = Depends(get_user_repository)
):
    use_case = LoginUserUseCase(repo)

    try:
        token = use_case.execute(dto)

        return TokenResponseDTO(access_token=token)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )