import re
from pydantic import BaseModel, Field, EmailStr, field_validator


class User(BaseModel):
    id: int = Field(unique=True)
    name: str = Field(min_length=1, max_length=50)
    username: str
    age: int = Field(gt=0)
    is_supervisor: bool
    email: EmailStr
    phone_number: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r"^\+\d{1}-\d{3}-\d{3}-\d{4}$", value):
            raise ValueError(
                "Номер телефона должен соответствовать формату: +7-000-000-0000"
            )
        return value


phone_number = "+7-612-345-6789"

is_valid = re.match(r"^\+\d{1}-\d{3}-\d{3}-\d{4}$", phone_number)

print(bool(is_valid))
