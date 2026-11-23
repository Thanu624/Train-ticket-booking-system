from typing import List
from sqlalchemy.orm import Session
from app.entities.user import User
from app.repositories.user_repository import UserRepository
from app.services.interfaces.user_service import IUserService
from app.dtos.user_dto import UserRegisterDto, UserLoginDto, UserUpdateDto, UserResponseDto, TokenResponseDto
from app.config.security import get_password_hash, verify_password, create_access_token
from app.exceptions.custom_exceptions import ConflictException, UnauthorizedException, NotFoundException


class UserServiceImpl(IUserService):
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, dto: UserRegisterDto) -> UserResponseDto:
        existing_user = self.user_repo.get_by_email(dto.email)
        if existing_user:
            raise ConflictException(f"User with email '{dto.email}' already exists")

        user = User(
            first_name=dto.first_name.strip(),
            last_name=dto.last_name.strip(),
            email=dto.email.strip().lower(),
            password=get_password_hash(dto.password),
            mobile_number=dto.mobile_number.strip(),
            role=dto.role,
        )
        self.user_repo.create(user)
        self.db.commit()
        self.db.refresh(user)
        return UserResponseDto.model_validate(user)

    def login(self, dto: UserLoginDto) -> TokenResponseDto:
        user = self.user_repo.get_by_email(dto.email)
        if not user or not verify_password(dto.password, user.password):
            raise UnauthorizedException("Invalid email or password")

        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role.value}
        )
        return TokenResponseDto(
            access_token=access_token,
            user=UserResponseDto.model_validate(user),
        )

    def get_user_by_id(self, user_id: int) -> UserResponseDto:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return UserResponseDto.model_validate(user)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponseDto]:
        users = self.user_repo.get_all(skip=skip, limit=limit)
        return [UserResponseDto.model_validate(u) for u in users]

    def update_user(self, user_id: int, dto: UserUpdateDto) -> UserResponseDto:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        if dto.first_name is not None:
            user.first_name = dto.first_name.strip()
        if dto.last_name is not None:
            user.last_name = dto.last_name.strip()
        if dto.mobile_number is not None:
            user.mobile_number = dto.mobile_number.strip()

        self.user_repo.update(user)
        self.db.commit()
        self.db.refresh(user)
        return UserResponseDto.model_validate(user)

    def delete_user(self, user_id: int) -> bool:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        self.user_repo.delete(user)
        self.db.commit()
        return True
