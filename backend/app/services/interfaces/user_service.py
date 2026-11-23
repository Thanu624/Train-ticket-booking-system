from abc import ABC, abstractmethod
from typing import List, Optional
from app.dtos.user_dto import UserRegisterDto, UserLoginDto, UserUpdateDto, UserResponseDto, TokenResponseDto


class IUserService(ABC):
    @abstractmethod
    def register(self, dto: UserRegisterDto) -> UserResponseDto:
        pass

    @abstractmethod
    def login(self, dto: UserLoginDto) -> TokenResponseDto:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> UserResponseDto:
        pass

    @abstractmethod
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponseDto]:
        pass

    @abstractmethod
    def update_user(self, user_id: int, dto: UserUpdateDto) -> UserResponseDto:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        pass
