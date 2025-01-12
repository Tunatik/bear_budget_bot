from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey, DECIMAL

from model_base import Base


class User(Base):

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str]
    accounts: Mapped['Account'] = relationship(back_populates='user', cascade='all, delete-orhan')
    transaction: Mapped['Transaction'] = relationship(back_populates='user', cascade='all, delete-orhan')


class Account(Base):

    name: Mapped[str]
    amount: Mapped[int]
    user: Mapped['User'] = relationship(back_populates='accounts')
    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'))


class Category(Base):
    __tablename__ = 'categories'
    __abstract__ = True

    name: Mapped[str]


class IncomeCategory(Category):
    __tablename__ = 'income_categories'

    type: Mapped[str] = mapped_column(default='Income')


class ExpenseCategory(Category):
    __tablename__ = 'expense_categories'
    type: Mapped[str] = mapped_column(default='Expense')


class Transaction(Base):

    amount: Mapped[float] = mapped_column(DECIMAL(12, 2))
    user: Mapped['User'] = relationship(back_populates='transaction')
    user_telegram_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'))



