import re
import pydantic as _pydantic


class _UserBase(_pydantic.BaseModel):
    email: str = _pydantic.Field(title="이메일")
    username: str = _pydantic.Field(title="이름", min_length=2, max_length=10)
    company_name: str = _pydantic.Field(title="회사명", min_length=2, max_length=20)

    @_pydantic.validator("email")
    def validate_email(cls, value):
        front_word, email = _pydantic.validate_email(value)

        if len(front_word) < 6:
            raise ValueError("이메일 기호(@) 앞 아이디를 6자리 이상 입력해주세요.")

        return email


class UserCreate(_UserBase):
    hashed_password: str = _pydantic.Field(title="비밀번호")
    confirm_password: str

    @_pydantic.root_validator
    def validate_password(cls, values):
        hashed_password = values.get("hashed_password")
        confirm_password = values.get("confirm_password")

        if hashed_password != confirm_password:
            raise ValueError("비밀번호가 일치하지 않습니다.")

        if not re.match(
            "^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{6,20}$", hashed_password
        ):
            raise ValueError("비밀번호에 특수문자와 알파벳이 각각 포함되어야 합니다.")

        return values

    class Config:
        orm_mode = True


class User(_UserBase):
    id: str
    is_active: bool
    is_staff: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class _PostBase(_pydantic.BaseModel):
    title: str
    content: str


class PostCreate(_PostBase):
    pass


class Post(_PostBase):
    id: int

    class Config:
        orm_mode = True
