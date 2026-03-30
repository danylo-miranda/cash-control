from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from cash_control.core.database import SessionLocal
from cash_control.application.dtos.user_dto import CreateUserDTO, UserResponseDTO
from cash_control.infrasctructure.repositories.user_repository_impl import UserRepositoryImpl
from cash_control.application.use_cases.create_user import CreateUserUseCase
from cash_control.api.v1.routes.auth_routes import router as auth_router
from cash_control.api.v1.routes.health_routes import router as health_router
from cash_control.api.v1.routes.user_routes import router as user_router

router = APIRouter()

router.include_router(user_router)
router.include_router(auth_router)
router.include_router(health_router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/users", response_model=UserResponseDTO)
def create_user(dto: CreateUserDTO, db: Session = Depends(get_db)):
    repo = UserRepositoryImpl(db)
    use_case = CreateUserUseCase(repo)
    user = use_case.execute(dto)
    
    return UserResponseDTO(
        id=1,
        name=user.name,
        email=user.email
    )    