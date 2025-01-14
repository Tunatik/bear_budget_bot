from pydantic import BaseModel


class TelegramIDModel(BaseModel):
    telegram_id: int


class UserModel(TelegramIDModel):
    username: str