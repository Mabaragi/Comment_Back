from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator
import re


class SignupReqeust(BaseModel):
    email: EmailStr = Field("회원가입 이메일 주소")
    name: str = Field(
        ..., description="사용자 이름 (2자 이상 10자 이하, 특수문자 및 공백 불가)"
    )
    password: str = Field(
        ..., description="비밀번호 (8자이상, 특수문자, 영문, 숫자 반드시 포함)"
    )

    @field_validator("name")
    def validate_name(cls, value):
        # 길이 조건 확인
        if not (2 <= len(value) <= 10):
            raise ValueError("이름은 2자 이상 10자 이하여야 합니다.")
        # 특수문자 및 공백 검증
        if not re.match(r"^[a-zA-Z가-힣0-9]+$", value):
            raise ValueError("이름에는 공백이나 특수문자를 포함할 수 없습니다.")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        # 8자 이상
        if not (8 <= len(value)):
            raise ValueError("비밀번호는 8자 이상이어야 합니다.")
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("비밀번호에는 영문이 포함되어야 합니다.")
        if not re.search(r"[0-9]", value):
            raise ValueError("비밀번호에는 숫자가 포함되어야 합니다.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("비밀번호에는 특수문자가 포함되어야 합니다.")
        return value


class SignupResponse(BaseModel):
    email: EmailStr
    name: str


class LoginRequest(BaseModel):
    email: EmailStr = Field(description="이메일")
    password: str = Field(description="비밀번호")
