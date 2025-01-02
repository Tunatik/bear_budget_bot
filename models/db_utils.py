from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import update, delete, select

from models.models import engine, Users, Transactions

with Session(engine) as session:
    db_session = session

def db_register_user(full_name: str, chat_id: int) -> bool:
    try:
        query = Users(full_name=full_name, telegram_id=chat_id)
        db_session.add(query)
        db_session.commit()
        return True
    except IntegrityError:
        db_session.rollback()
        return False

def db_add_income(amount: int):
    query = Transactions(type='Income', amount=amount)
    db_session.add(query)
    db_session.commit()

def db_add_expenses(amount: int):
    query = Transactions(type='Expenses', amount=-amount)
    db_session.add(query)
    db_session.commit()