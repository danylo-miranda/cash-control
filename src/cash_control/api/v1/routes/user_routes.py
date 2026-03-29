from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from cash_control.core.database import SessionLocal
from cash_control.application.dtos.user_dto import CreateUserDTO, UserResponseDTO
from cash_control.infrasctructure.repositories.user_repository_impl import UserRepositoryImpl
from cash_control.application.use_cases.create_user import CreateUserUseCase

router = APIRouter(prefix="/users", tags=["Users"])


# 🔌 Dependency - DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔌 Dependency - Repository
def get_user_repository(db: Session = Depends(get_db)):
    return UserRepositoryImpl(db)


# 🚀 CREATE USER
@router.post(
    "/",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    dto: CreateUserDTO,
    repo: UserRepositoryImpl = Depends(get_user_repository)
):
    use_case = CreateUserUseCase(repo)

    try:
        user = use_case.execute(dto)
        return UserResponseDTO(
            id=1,  # ⚠️ ajustar quando retornar ID real do banco
            name=user.name,
            email=user.email
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# 🔍 GET USER BY EMAIL (exemplo)
@router.get(
    "/by-email/{email}",
    response_model=UserResponseDTO
)
def get_user_by_email(
    email: str,
    repo: UserRepositoryImpl = Depends(get_user_repository)
):
    user = repo.get_by_email(email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponseDTO(
        id=1,
        name=user.name,
        email=user.email
    )


# 📄 LIST USERS (mock simples)
@router.get("/", response_model=list[UserResponseDTO])
def list_users(
    repo: UserRepositoryImpl = Depends(get_user_repository)
):
    users = getattr(repo, "db", [])  # fallback mock

    return [
        UserResponseDTO(
            id=i + 1,
            name=user.name,
            email=user.email
        )
        for i, user in enumerate(users)
    ]