from sqlalchemy.orm import Session
from cash_control.domain.entities.user import User
from cash_control.domain.interfaces.user_repository import UserRepository
from cash_control.infrasctructure.models.user_models import UserModel

class UserRepositoryImpl(UserRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
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

    def get_by_email(self, email: str) -> User | None:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()

        if not model:
            return None

        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            hashed_password=model.password
        )
        
    def list_all(self) -> list[User]:
        models =self.db.query(UserModel).all()
        return [
            User(
                id=model.id,
                name=model.name,
                email=model.email,
                hashed_password=model.password
            )
            for model in models
        ]