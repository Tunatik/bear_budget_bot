from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete, update, func
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from dao.model_base import Base


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel):
        """Find one record by the given filters"""
        filters_dict = filters.model_dump(exclude_unset=True)
        logger.info(f'Search for the single entry {cls.model.__name__} by filters {filters_dict}')

        try:
            query = select(cls.model).filter_by(**filters_dict)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info('Record found')
            else:
                logger.info('Record not found')

            return record
        except SQLAlchemyError as e:
            logger.error(f'Error while searching for a record: {e}')
            raise

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel):
        """Add one record"""
        values_dict = values.model_dump()
        logger.info(f'Adding record {cls.model.__name__} with values {values_dict}')

        new_instance = cls.model(**values_dict)
        session.add(new_instance)

        try:
            await session.flush()
            logger.info('Record successfully added')
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f'Error while adding record: {e}')
            raise e