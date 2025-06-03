from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from src.infrastructure.data_sources.db.models import User
from src.domain.repositories.i_user_repository import IUserRepository
from src.domain.entities.user_entities import UserProfileEntity
from src.infrastructure.utils.logger import setup_logger

logger = setup_logger('user_db_repository')

class UserDBRepository(IUserRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory


    def get_all(self) -> list[UserProfileEntity]:
        with self.session_factory() as session:
            users = session.query(User).all()
            return [
                UserProfileEntity(
                    id=str(user.id),
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    profile_pic=user.profile_pic
                ) for user in users
            ]


    def get_by_id(self, user_id: str) -> UserProfileEntity:
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise UserNotFoundError(user_id)
            return UserProfileEntity(
                id=str(user.id),
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                profile_pic=user.profile_pic
            )


    def get_by_email(self, email: str) -> UserProfileEntity:
        with self.session_factory() as session:
            user = session.query(User).filter(User.email == email).first()
            if not user:
                raise UserNotFoundError(email)
            return UserProfileEntity(
                id=str(user.id),
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                profile_pic=user.profile_pic
            )


    def add(
        self,
        id: str,
        email: str,
        first_name: str = None,
        last_name: str = None,
        profile_pic: str = None,
    ) -> UserProfileEntity:
        with self.session_factory() as session:
            user = User(
                id=id,
                email=email,
                first_name=first_name,
                last_name=last_name,
                profile_pic=profile_pic,
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            logger.info(f"User created: {user}")
            return UserProfileEntity(
                id=str(user.id),
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                profile_pic=user.profile_pic
            )


    def delete_by_id(self, user_id: str) -> UserProfileEntity:
        with self.session_factory() as session:
            entity: User = session.query(User).filter(User.id == user_id).first()
            if not entity:
                raise UserNotFoundError(user_id)
            session.delete(entity)
            session.commit()
            return UserProfileEntity(
                id=str(entity.id),
                email=entity.email,
                first_name=entity.first_name,
                last_name=entity.last_name,
                profile_pic=entity.profile_pic
            )


    def delete_by_email(self, email: str) -> UserProfileEntity:
        with self.session_factory() as session:
            entity: User = session.query(User).filter(User.email == email).first()
            if not entity:
                raise UserNotFoundError(email)
            session.delete(entity)
            session.commit()
            return UserProfileEntity(
                id=str(entity.id),
                email=entity.email,
                first_name=entity.first_name,
                last_name=entity.last_name,
                profile_pic=entity.profile_pic
            )


    def update_by_id(
        self,
        user_id: str,
        first_name: str = None,
        last_name: str = None,
        profile_pic: str = None,
    ) -> UserProfileEntity:
        with self.session_factory() as session:
            entity: User = session.query(User).filter(User.id == user_id).first()
            if not entity:
                raise UserNotFoundError(user_id)
            entity.first_name = first_name if first_name else entity.first_name
            entity.last_name = last_name if last_name else entity.last_name
            entity.profile_pic = profile_pic if profile_pic else entity.profile_pic
            session.commit()
            session.refresh(entity)
            return UserProfileEntity(
                id=str(entity.id),
                email=entity.email,
                first_name=entity.first_name,
                last_name=entity.last_name,
                profile_pic=entity.profile_pic
            )


    def update_by_email(
        self,
        email: str,
        first_name: str = None,
        last_name: str = None,
        profile_pic: str = None,
    ) -> UserProfileEntity:
        with self.session_factory() as session:
            entity: User = session.query(User).filter(User.email == email).first()
            if not entity:
                raise UserNotFoundError(email)
            entity.first_name = first_name if first_name else entity.first_name
            entity.last_name = last_name if last_name else entity.last_name
            entity.profile_pic = profile_pic if profile_pic else entity.profile_pic
            session.commit()
            session.refresh(entity)
            return UserProfileEntity(
                id=str(entity.id),
                email=entity.email,
                first_name=entity.first_name,
                last_name=entity.last_name,
                profile_pic=entity.profile_pic
            )


class NotFoundError(Exception):

    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, {entity_id}")


class UserNotFoundError(NotFoundError):

    entity_name: str = "User"