from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from cash_control.core.database import SessionLocal
from cash_control.application.dtos.user_dto import CreateUserDTO, UserResponseDTO
from cash_control.domain.entities.user import User
from cash_control.infrasctructure.repositories.user_repository_impl import UserRepositoryImpl
from cash_control.application.use_cases.create_user import CreateUserUseCase
from cash_control.infrasctructure.models.user_models import UserModel
from cash_control.core.deps import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


# Dependency - DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency - Repository
def get_user_repository(db: Session = Depends(get_db)):
    return UserRepositoryImpl(db)

# PROTEC ROUTES
@router.get("/secure")
def protected_route(user=Depends(get_current_user)):
    return {
        "message": "Access granted",
        "user": user
    }

# CREATE USER
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
            id=user.id,  
            name=user.name,
            email=user.email
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

def create(self, user: User) -> User:
    try:
        model = UserModel(
            name=user.name,
            email=user.email,
            password=user.hashed_password
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            hashed_password=model.password
        )

    except IntegrityError:
        self.db.rollback()
        raise ValueError("Email already registered")

# GET USER BY EMAIL (exemplo)
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
        id=user.id,
        name=user.name,
        email=user.email
    )


# LIST USERS (mock simples)
@router.get("/", response_model=list[UserResponseDTO])
def list_users(
    repo: UserRepositoryImpl = Depends(get_user_repository)
):
    users = repo.list_all()

    return [
        UserResponseDTO(
            id=user.id,
            name=user.name,
            email=user.email
        )
        for user in users
    ]