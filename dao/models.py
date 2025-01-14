from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey, DECIMAL

from dao.model_base import Base


class User(Base):

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str]
    accounts: Mapped[List['Account']] = relationship(back_populates='user', cascade='all, delete-orphan')
    transactions: Mapped[List['Transaction']] = relationship(back_populates='user', cascade='all, delete-orphan')
    categories: Mapped[List['Category']] = relationship(back_populates='user', cascade='all, delete-orphan')


class Account(Base):

    name: Mapped[str]
    amount: Mapped[int] = mapped_column(default=0)
    user: Mapped['User'] = relationship(back_populates='accounts')
    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'))


class Category(Base):
    __tablename__ = 'categories'

    name: Mapped[str]
    type: Mapped[str]
    user: Mapped['User'] = relationship(back_populates='categories')
    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'))
    transactions: Mapped[List['Transaction']] = relationship(back_populates='category')


class Transaction(Base):

    amount: Mapped[float] = mapped_column(DECIMAL(12, 2))
    category: Mapped['Category'] = relationship(back_populates='transactions')
    category_type: Mapped[str] = mapped_column(ForeignKey('categories.type'))
    user: Mapped['User'] = relationship(back_populates='transactions')
    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'))



