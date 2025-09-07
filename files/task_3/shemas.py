import re
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator,
    ValidationError,
    ConfigDict,
)
from pydantic.alias_generators import to_camel
from pydantic.dataclasses import dataclass
from enum import Enum
from typing import Any
from datetime import date
from settings.settings import settings

list_storage = []


class User(BaseModel):
    id: int = Field(
        title="Уникальный идентификатор пользователя",
        description="Позволяет упорядочить пользователей",
    )
    name: str = Field(
        min_length=1,
        max_length=50,
        title="Имя пользователя",
        description="Имя пользователя",
    )
    username: str = Field(
        title="Никнейм пользователя",
        description="Используется Oauth",
        default=str(id) + str(name),
    )
    age: int = Field(gt=0, title="Возраст", description="Возраст пользователя")
    is_supervisor: bool = Field(
        title="Является ли админом", description="Проверка на суперпользователя"
    )
    email: EmailStr = Field(title="Электронная почта", description="Электронная почта")
    phone_number: str = Field(title="Номер телефона", description="Номер телефона")
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
    PURCHASE = "PURCHASE"
    SELL = "SELL"


class Deal(BaseModel):
    """
    Модель сделки
    """

    id: int | None = Field(
        default=None,
        title="Уникальный идентификатор пользователя",
        description="Позволяет упорядочить пользователей",
    )
    title: str | None = Field(
        default=None, title="Название сделки", description="Название сделки"
    )
    comment: str | None = Field(
        default=None, title="Комментарий к сделке", description="Комментарий к сделке"
    )
    created_at: date = Field(
        default=date.today(),
        title="Дата заключения сделки",
        description="Дата заключения сделки",
    )
    persons_in_charge: list[str] | None = Field(
        default=None,
        title="Список ответственных лиц",
        description="Список ответственных лиц",
    )
    deal_type: DealType | None = Field(
        default=None, title="Тип сделки", description="Тип сделки"
    )
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        list_storage.append(self.id)

    def update(self, new_data: dict):
        for k, v in new_data.items():
            setattr(self, k, v)

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: int) -> int:
        if value in list_storage:
            raise ValueError(
                "Значение идентификатора пользователя должно быть уникальным!"
            )
        return value

    @field_validator("created_at")
    @classmethod
    def validate_created_at(cls, value: date) -> date:
        if value < date.today():
            raise ValueError("Дата создания не может быть раньше сегодняшнего дня")
        return value


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


@dataclass
class DealsStore(metaclass=SingletonMeta):
    """
    Хранилище сделок
    """

    _deals_data = []

    @property
    def deals_data(self):
        return self._deals_data

    @deals_data.setter
    def deals_data(self, data):
        self._deals_data.append(data)


class DatabaseConnection:
    """
    Контекстный менеджер, имитирующий подключение к БД
    """

    def __init__(self, db_url):
        self.db_url = db_url

    def __enter__(self):
        try:
            print(f"Подключение к базе данных с URL: {settings.db_url}")
            self.conn = db_immitation.connect(self.db_url)
            print("Подключение к базе данных установлено!")
            return self.conn
        except NameError:
            print("Иммитация работы с БД...")

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            print(f"Отключение от базы данных с URL: {settings.db_url}")
            self.conn.close()
            print("Отключение от базы данных")
        except AttributeError:
            print("Иммитация работы с БД...")


class DealsRepository:
    def __init__(self, deal_models: list[Deal], connection: DatabaseConnection):
        self.__deal_models = deal_models
        self.__connection = connection

    @property
    def deal_models(self):
        return self.__deal_models

    @deal_models.setter
    def deal_models(self, deal_models: list[Deal]):
        self.__deal_models = deal_models

    @deal_models.deleter
    def deal_models(self):
        del self.__deal_models

    @property
    def connection(self):
        return self.__connection

    @connection.setter
    def connection(self, connection: DatabaseConnection):
        self.__connection = connection

    @connection.deleter
    def connection(self):
        del self.__connection

    def create_deal(self):
        with self.__connection:
            for i in self.__deal_models:
                try:
                    DealsStore.deals_data(i)
                except ValidationError as e:
                    print(e)

    def get_deals_dicts(self) -> list[dict]:
        list_of_deal_dicts = []
        with self.__connection:
            for i in self.__deal_models:
                try:
                    model_dict = i.model_dump()
                    list_of_deal_dicts.append(model_dict)
                except Exception as e:
                    print(e)
            return list_of_deal_dicts

    def get_deal(self, deal_id: int) -> Deal:
        with self.__connection:
            for i in self.__deal_models:
                try:
                    if i.id == deal_id:
                        return i
                except Exception as e:
                    print(e)

    def delete_deal(self, deal_id: int):
        with self.__connection:
            for i in self.__deal_models:
                try:
                    if i.id == deal_id:
                        del i
                except Exception as e:
                    print(e)

    def update_deal(self, deal_id: int, update_data: dict):
        with self.__connection:
            for i in self.__deal_models:
                try:
                    if i.id == deal_id:
                        i.update(update_data)
                        return i
                except Exception as e:
                    print(e)
