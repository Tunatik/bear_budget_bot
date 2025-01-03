import datetime
from os import getenv
from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, Session, mapped_column
from sqlalchemy import String, Integer, BigInteger, DECIMAL, ForeignKey, DATE, text
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_ADDRESS = getenv('DB_ADDRESS')
DB_NAME = getenv('DB_NAME')

engine = create_engine(f'sqlite:///./bear_budget_db.db', echo=True)

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.now(datetime.UTC),
    )]


class Base(DeclarativeBase):
    pass


class Users(Base):
    """Table for users"""

    __tablename__ = 'users'

    id: Mapped[intpk]
    full_name: Mapped[str] = mapped_column(String(128))
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)


class Transactions(Base):
    """Table for transactions"""

    __tablename__ = 'transactions'

    id: Mapped[intpk]
    type: Mapped[str] = mapped_column(String(20))
    amount: Mapped[int] = mapped_column(DECIMAL(12, 2), default=0)


class Accounts(Base):
    """Table for accounts"""

    __tablename__ = 'accounts'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(50))
    amount: Mapped[int] = mapped_column(DECIMAL(12, 2), default=0)


class Categories(Base):
    """Table for categories"""

    __tablename__ = 'categories'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(50))

