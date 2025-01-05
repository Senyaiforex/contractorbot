from sqlalchemy import select

from models import Service
from database import get_async_session

async def create_services():
    async for session in get_async_session():
        query = await session.execute(select(Service))
        sedvice_inst = query.scalars().first()
        if sedvice_inst:
            return
        list_services = ['Лестницы бетонные', 'Навесы', 'Металлоконструкции (лестницы, заборы, ворота, антресоли, ангары и пр.)',
                         'Обшивка лестниц деревом / керамогранииом', 'Окна ПВХ', 'Двери', 'Вентиляция',
                         'Полы', 'Потолки', 'Каменные работы', 'Стяжка', 'Электрика', 'Сантехника', 'Корпусная мебель']
        for service in list_services:
            new_instance = Service(name=service)
            session.add(new_instance)
            await session.commit()