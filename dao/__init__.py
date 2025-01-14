from dao.dao_base import BaseDAO
from dao.models import User, Transaction, Account, Category


class UserDAO(BaseDAO):
    model = User


class TransactionDAO(BaseDAO):
    model = Transaction


class AccountDAO(BaseDAO):
    model = Account


class CategoryDAO(BaseDAO):
    model = Category