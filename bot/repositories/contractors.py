from sqlalchemy import select, and_, or_, update

from database import get_async_session, AsyncSession
from models import Contractors, Service, services_contractors
from functools import wraps
from .decorators import base_session


class ContractRepository:
    """
    Репозиторий для работы с моделями подрядчика
    """

    @classmethod
    @base_session
    async def get_all_contractors(cls, session: AsyncSession) -> list[Contractors]:
        query = await session.execute(select(Contractors))
        contractors = query.scalars().all()
        return contractors

    @classmethod
    @base_session
    async def get_contractor_by_id(cls, id_telegram: int, session: AsyncSession) -> Contractors | None:
        query = await session.execute(select(Contractors).where(Contractors.id_telegram == id_telegram))
        contractor = query.scalar_one_or_none()
        return contractor

    @classmethod
    @base_session
    async def add_service(cls, id_telegram: int, service_id: int, session: AsyncSession) -> None:
        await session.execute(services_contractors.insert().values(
                id_telegram=id_telegram,
                service_id=service_id
        ))
        await session.commit()

    @classmethod
    @base_session
    async def del_service(cls, id_telegram: int, service_id: int, session: AsyncSession) -> None:
        query = (services_contractors.delete().where(and_(services_contractors.c.id_telegram == id_telegram,
                                                          services_contractors.c.service_id == service_id)))
        await session.execute(query)
        await session.commit()

    @classmethod
    @base_session
    async def create_contr(cls, id_telegram: int, user_name: str, fio: str, session: AsyncSession) -> None:
        new_inst = Contractors(id_telegram=id_telegram, user_name=user_name, full_name=fio)
        session.add(new_inst)
        await session.commit()

    @classmethod
    @base_session
    async def get_contractor_with_services(cls, id_telegram: int, session: AsyncSession) -> Contractors | None:
        query = await session.execute(select(Contractors).where(Contractors.id_telegram == id_telegram))
        contractor = query.scalar_one_or_none()
        return contractor

    @classmethod
    @base_session
    async def get_contractors_by_service(cls, name_service: str, session: AsyncSession) -> list[Contractors]:
        query = (
                select(
                        Contractors)
                .join(services_contractors)
                .join(Service)
                .where(and_(Service.name == name_service, or_(Contractors.balance > 0, Contractors.free_try == True)))
        )
        result = await session.execute(query)
        contractors = result.scalars().all()
        return contractors

    @classmethod
    @base_session
    async def update_contractor(cls, contr_id: int, data: dict, session: AsyncSession) -> None:
        """
        Обновление параметра
        :param contr_id: ID телеграм подрядчика
        :param data: Данные для обновления
        :param session: Асинхронная сессия
        :return: None
        """
        stmt = (
                update(Contractors).
                where(Contractors.id_telegram == contr_id).
                values(**data)
        )
        await session.execute(stmt)
        await session.commit()
    @classmethod
    @base_session
    async def get_contractors_for_order(cls, service_id: int, session: AsyncSession) -> list[Contractors] | None:
        """
        Обновление параметра
        :param session: Асинхронная сессия
        :return: None
        """
        stmt = (
                select(Contractors)
                .join(services_contractors, services_contractors.c.id_telegram == Contractors.id_telegram)
                .where(
                        and_(
                                or_(Contractors.free_try == True, Contractors.balance >= 100),
                                services_contractors.c.service_id == service_id
                        )
        ))
        query = await session.execute(stmt)
        contractors = query.scalars().all()
        return contractors
    @classmethod
    @base_session
    async def decrease_balance(cls, id_telegram: int, value: int, session: AsyncSession) -> None:
        stmt = update(Contractors).where(Contractors.id_telegram == id_telegram).values(balance=Contractors.balance - value)
        await session.execute(stmt)
        await session.commit()
    @classmethod
    @base_session
    async def up_balance(cls, id_telegram: int, value: int, session: AsyncSession) -> None:
        stmt = update(Contractors).where(Contractors.id_telegram == id_telegram).values(balance=Contractors.balance + value)
        await session.execute(stmt)
        await session.commit()