from os import getenv

from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, Session, mapped_column
from sqlalchemy import String, Integer, BigInteger, DECIMAL, ForeignKey, DATE
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_ADDRESS = getenv('DB_ADDRESS')
DB_NAME = getenv('DB_NAME')

engine = create_engine(f'sqlite:///bear_budget_db.db')


class Base(DeclarativeBase):
    pass


class Users(Base):
    """Table for users"""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)


class Transactions(Base):
    """Table for transactions"""

    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(20))
    amount: Mapped[int] = mapped_column(DECIMAL(12, 2), default=0)



