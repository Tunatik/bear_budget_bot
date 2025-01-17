from pydantic import BaseModel


class TelegramIDModel(BaseModel):
    telegram_id: int


class UserModel(TelegramIDModel):
    username: str


class CategoryModel(BaseModel):
    name: str | None
    type: str | None
    telegram_id: int | None


class CategoryIDModel(BaseModel):
    id: int


class CategoryNameModel(BaseModel):
    name: str

class CategoryTypeModel(BaseModel):
    type: str