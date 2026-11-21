import requests
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> User:
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )
        return self.repository.create(user_data)

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        user = self.get_user(user_id)
        if user_data.email and user_data.email != user.email:
            existing_user = self.repository.get_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email is already in use by another user",
                )
        return self.repository.update(user, user_data)

    def register_user(self, user_id: int) -> User:
        user = self.get_user(user_id)
        return self.repository.set_registered(user, True)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)

        # מחיקת תשובות המשתמש ב-Poll Service דרך API
        try:
            response = requests.delete(
                f"{settings.POLL_SERVICE_URL}/answers/user/{user_id}",
                timeout=5,
            )
            if response.status_code not in (200, 204, 404):
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Failed to delete user answers in Poll Service",
                )
        except requests.RequestException as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Poll Service is unavailable",
            ) from exc

        self.repository.delete(user)