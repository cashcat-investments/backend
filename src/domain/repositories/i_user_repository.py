from abc import ABC, abstractmethod
from src.domain.entities.user_entities import UserProfileEntity

class IUserRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[UserProfileEntity]:
        pass


    @abstractmethod
    def get_by_id(self, user_id: str) -> UserProfileEntity:
        pass


    @abstractmethod
    def get_by_email(self, email: str) -> UserProfileEntity:
        pass


    @abstractmethod
    def add(
        self,
        id: str,
        email: str,
        first_name: str = None,
        last_name: str = None,
        profile_pic: str = None,
    ) -> UserProfileEntity:
        pass


    @abstractmethod
    def delete_by_id(self, user_id: str) -> UserProfileEntity:
        pass


    @abstractmethod
    def delete_by_email(self, email: str) -> UserProfileEntity:
        pass
    
    @abstractmethod
    def update_by_id(
        self,
        user_id: str,
        first_name: str = None,
        last_name: str = None,
        profile_pic: str = None,
    ) -> UserProfileEntity:
        pass


    @abstractmethod
    def update_by_email(
        self,
        email: str,
        first_name: str = None,
        last_name: str = None,
        profile_pic: str = None,
    ) -> UserProfileEntity:
        pass