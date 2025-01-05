from sqlalchemy import select, and_, or_, delete

from database import get_async_session, AsyncSession
from models import Contractors, Service, services_contractors
from functools import wraps
from .decorators import base_session


class ServiceRepository:
    """
    Репозиторий для работы с моделями услуги
    """

    @classmethod
    @base_session
    async def get_all_services(cls, session: AsyncSession) -> list[Service]:
        query = await session.execute(select(Service))
        services = query.scalars().all()
        return services

    @classmethod
    @base_session
    async def get_service_by_name(cls, name_service: str, session: AsyncSession) -> Service | None:
        query = await session.execute(select(Service).where(Service.name == name_service))
        service = query.scalar_one_or_none()
        return service

    @classmethod
    @base_session
    async def get_service_by_id(cls, id_service: int, session: AsyncSession) -> Service | None:
        query = await session.execute(select(Service).where(Service.id == id_service))
        service = query.scalar_one_or_none()
        return service

    @classmethod
    @base_session
    async def get_services_by_contractor(cls, id_contractor: int, session: AsyncSession) -> list[Service]:
        query = (
                select(
                        Service)
                .join(services_contractors)
                .join(Contractors)
                .where(Contractors.id_telegram == id_contractor)
        )
        result = await session.execute(query)
        services = result.scalars().all()
        return services
    @classmethod
    @base_session
    async def del_service_admin(cls, service_id: int, session: AsyncSession) -> None:
        query = (
                delete(Service)
                .where(Service.id == service_id)
        )
        await session.execute(query)
        await session.commit()

    @classmethod
    @base_session
    async def add_service_admin(cls, service_name: str, session: AsyncSession) -> None:
        new_service = Service(name=service_name)
        session.add(new_service)
        await session.commit()

