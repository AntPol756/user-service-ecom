from typing import Optional
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user_data: UserCreate) -> User:
        db_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            age=user_data.age,
            address=user_data.address,
            is_registered=False,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user: User, user_data: UserUpdate) -> User:
        update_fields = user_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def set_registered(self, user: User, is_registered: bool = True) -> User:
        user.is_registered = is_registered
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()