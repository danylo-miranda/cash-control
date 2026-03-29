from sqlalchemy.orm import Session
from cash_control.domain.entities.user import User
from cash_control.domain.interfaces.user_repository import UserRepository
from cash_control.infrasctructure.models.user_models import UserModel

class UserRepositoryImpl(UserRepository):
    
    def __init__(self, db: Session):
        self.db = db
        
        def create(self, user: User):
            model = UserModel(
                name=user.name,
                email=user.email,
                password=user.hashed_password
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return User
