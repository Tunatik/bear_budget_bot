from pydantic import BaseModel


class TelegramIDModel(BaseModel):
    telegram_id: int


class UserModel(TelegramIDModel):
    username: str


class CategoryModel(BaseModel):
    name: str
    type: str
    user_telegram_id: int