from enum import Enum
from typing import final
from fastapi import Request
from .structors import LocalProxy
from .structors import LocalStack
from dataclasses import dataclass
from dataclasses import KW_ONLY, dataclass, field


@final
class Messages(LocalStack):
    pass

@final
class Requests(LocalStack):
    pass


message_context = Messages()
request_context = Requests()

message: LocalProxy = LocalProxy[Messages](
    message_context, context=False, stackable=True
)
request: Request = LocalProxy[Request](request_context, context=True, stackable=False) # type: ignore


class BaseModel:
    def jsonifier(self) -> dict[str, str]:
        fields: dict[str, BaseModel] = self.__dict__
        row: dict = dict()
        for key, field in fields.items():
            row[key] = field if not isinstance(field, BaseModel) else field.jsonifier()
        return row


@dataclass
class UserPermissions(BaseModel):
    is_authenticated: bool=False
    is_golden: bool=False
    is_blue: bool=False
    is_red: bool=False
    is_staff: bool=False
    is_admin: bool=False

# class UserType(Enum):
    
@dataclass
class UserProfile(BaseModel):
    email: str | None
    phone: str | None
    type: int
    permissions: UserPermissions


@dataclass
class UserModel(BaseModel):
    id: int = field(init=False)
    _: KW_ONLY
    sub: str | int
    name: str | None
    profile: UserProfile

    def __post_init__(self) -> None:
        self.id = int(self.sub)
        self.profile.type = int(self.profile.type)


@dataclass
class SupporterModel:
    id: str | int = field(init=False)
    _: KW_ONLY
    sub: str | int
    name: str

    def __post_init__(self) -> None:
        self.id = self.sub

