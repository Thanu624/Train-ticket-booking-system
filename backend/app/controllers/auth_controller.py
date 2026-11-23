from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.auth_deps import get_current_user
from app.entities.user import User
from app.services.impl.user_service_impl import UserServiceImpl
from app.dtos.user_dto import UserRegisterDto, UserLoginDto, UserResponseDto, TokenResponseDto
from app.dtos.common_dto import ApiResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=ApiResponse[UserResponseDto], status_code=status.HTTP_201_CREATED)
def register(dto: UserRegisterDto, db: Session = Depends(get_db)):
    service = UserServiceImpl(db)
    user = service.register(dto)
    return ApiResponse(message="User registered successfully", data=user)


@router.post("/login", response_model=ApiResponse[TokenResponseDto])
def login(dto: UserLoginDto, db: Session = Depends(get_db)):
    service = UserServiceImpl(db)
    token = service.login(dto)
    return ApiResponse(message="Login successful", data=token)


@router.get("/me", response_model=ApiResponse[UserResponseDto])
def get_current_profile(current_user: User = Depends(get_current_user)):
    return ApiResponse(
        message="Current user fetched",
        data=UserResponseDto.model_validate(current_user),
    )
