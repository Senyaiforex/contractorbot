from sqlalchemy import select, and_, or_, update, func
from sqlalchemy.orm import selectinload

from database import get_async_session, AsyncSession
from models import Order, StatusEnum
from functools import wraps
from .decorators import base_session
from datetime import date, timedelta

class OrderRepository:
    """
    Репозиторий для работы с моделями заявки
    """

    @classmethod
    @base_session
    async def create_order(cls, text: str, session: AsyncSession) -> Order:
        new_inst = Order(description=text)
        session.add(new_inst)
        await session.commit()
        await session.refresh(new_inst)
        return new_inst

    @classmethod
    @base_session
    async def update_photo_order(cls, order_id: int, photo: str, session: AsyncSession) -> None:
        stmt = (
                update(Order).
                where(Order.id == order_id).
                values({'photo_path': photo})
        )
        await session.execute(stmt)
        await session.commit()

    @classmethod
    @base_session
    async def get_orders_by_user(cls, id_telegram: int, type_order: str,
                                 session: AsyncSession) -> list[Order] | None:
        if type_order == 'all':
            query = await session.execute(select(Order)
                                      .options(selectinload(Order.service))
                                      .where(Order.user_telegram == id_telegram)
                                      .order_by(Order.date.desc()))
        elif type_order == 'active':
            query = await session.execute(select(Order)
                                          .options(selectinload(Order.service))
                                          .where(and_(Order.user_telegram == id_telegram,
                                                      Order.status  == StatusEnum.active))
                                          .order_by(Order.date.desc()))
        else:
            query = await session.execute(select(Order)
                                          .options(selectinload(Order.service))
                                          .where(and_(Order.user_telegram == id_telegram,
                                                      Order.status  == StatusEnum.completed))
                                          .order_by(Order.date.desc()))
        orders = query.scalars().all()
        return orders

    @classmethod
    @base_session
    async def add_service_to_order(cls, id_order: int, id_service: int, session: AsyncSession) -> None:
        query = await session.execute(
                update(Order).
                where(Order.id == id_order).
                values({'service_id': id_service})
        )
        await session.commit()

    @classmethod
    @base_session
    async def get_order_by_id(cls, id_order: int, session: AsyncSession) -> Order | None:
        query = await session.execute(select(Order)
                                      .options(selectinload(Order.service))
                                      .where(Order.id == id_order))
        orders = query.scalars().first()
        return orders

    @classmethod
    @base_session
    async def add_user_in_order(cls, id_order: int, user_telegram: int, session: AsyncSession) -> Order | None:
        query = await session.execute(
                update(Order).
                where(Order.id == id_order).
                values({'user_telegram': user_telegram})
        )
        await session.commit()

    @classmethod
    @base_session
    async def update_data_order(cls, order_id: int, data: dict, session: AsyncSession) -> None:
        stmt = (
                update(Order).
                where(Order.id == order_id).
                values(data)
        )
        await session.execute(stmt)
        await session.commit()
    @classmethod
    @base_session
    async def get_active_orders(cls, session: AsyncSession) -> list[Order] | None:
        query = await session.execute(select(Order)
                                      .options(selectinload(Order.service))
                                      .where(and_(Order.user_telegram == None,
                                                  Order.status == StatusEnum.active)))
        orders = query.scalars().first()
        return orders
    @classmethod
    @base_session
    async def get_orders_date(cls, date: date, session: AsyncSession) -> tuple[int]:
        """
        Функция для получения количества созданных заказов
        за сегодняшний день, неделю, месяц
        :param session: Асинхронная сессия
        :param date: Дата
        :return: Количество пользователей
        :rtype: tuple[int]
        """
        week_date = date - timedelta(days=7)
        month_date = date - timedelta(days=30)
        count_today = await session.execute(
                select(func.count(Order.id))
                .where(Order.date == date)
        )
        count_week = await session.execute(
                select(func.count(Order.id))
                .where(Order.date >= week_date)
        )
        count_month = await session.execute(
                select(func.count(Order.id))
                .where(Order.date >= month_date)
        )
        return (count_today.scalar(), count_week.scalar(), count_month.scalar())
    @classmethod
    @base_session
    async def get_count_orders(cls, session: AsyncSession) -> list[tuple[int, str]]:
        count_active_orders = await session.execute(
                select(func.count(Order.id))
                .where(Order.status == StatusEnum.active)
        )
        count_completed_orders = await session.execute(
                select(func.count(Order.id))
                .where(Order.status == StatusEnum.completed)
        )
        return (count_active_orders.scalar(), count_completed_orders.scalar())