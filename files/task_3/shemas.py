import re
from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationError, ConfigDict
from pydantic.alias_generators import to_camel
from enum import Enum
from typing import Any
from datetime import date

list_storage = []


class User(BaseModel):
    id: int = Field(title='Уникальный идентификатор пользователя', description='Позволяет упорядочить пользователей')
    name: str = Field(min_length=1, max_length=50, title='Имя пользователя', description='Имя пользователя')
    username: str = Field(title='Никнейм пользователя', description='Используется Oauth', default=str(id)+str(name))
    age: int = Field(gt=0, title='Возраст', description='Возраст пользователя')
    is_supervisor: bool = Field(title='Является ли админом', description='Проверка на суперпользователя')
    email: EmailStr = Field(title='Электронная почта', description='Электронная почта')
    phone_number: str = Field(title='Номер телефона', description='Номер телефона')
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        list_storage.append(self.id)

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: int) -> int:
        if value in list_storage:
            raise ValueError(
                "Значение идентификатора пользователя должно быть уникальным!"
            )
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r"^\+\d{1} \(\d{3}\) \d{3}-\d{2}-\d{2}$", value):
            raise ValueError(
                "Номер телефона должен соответствовать формату: +7 (000) 000-00-00"
            )
        return value



class DealType(Enum):
    PURCHASE = 'PURCHASE'
    SELL = 'SELL'


class Deal(BaseModel):
    id: int = Field(title='Уникальный идентификатор пользователя', description='Позволяет упорядочить пользователей')
    title: str = Field(title='Название сделки', description='Название сделки')
    comment: str = Field(title='Комментарий к сделке', description='Комментарий к сделке')
    created_at: date = Field(default=date.today(), title='Дата заключения сделки', description='Дата заключения сделки')
    persons_in_charge: list[str] = Field(title='Список ответственных лиц', description='Список ответственных лиц')
    deal_type: DealType = Field(title='Тип сделки', description='Тип сделки')
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        list_storage.append(self.id)


    @field_validator("id")
    @classmethod
    def validate_id(cls, value: int) -> int:
        if value in list_storage:
            raise ValueError(
                "Значение идентификатора пользователя должно быть уникальным!"
            )
        return value

    @field_validator('created_at')
    @classmethod
    def validate_created_at(cls, value: date) -> date:
        if value < date.today():
            raise ValueError(
                "Дата создания не может быть раньше сегодняшнего дня"
            )
        return value



try:
    user = Deal(
        id=123,
        title='title',
        comment='comment',
        created_at='2025-09-08',
        persons_in_charge=['steve', 'bob'],
        deal_type=DealType.PURCHASE
    )
except ValidationError as e:
    print(e)