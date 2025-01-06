import asyncio
import datetime
import os
import pandas as pd
from sqlalchemy import func, select, String, cast, case

from models import Service, Order, Contractors, StatusEnum, services_contractors
from repositories import ContractRepository, OrderRepository, ServiceRepository
from database import get_async_session
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_services_text(services: list[Service]) -> str:
    """
    Формирует текстовое описание услуг
    :param services: список услуг
    :return: текстовое описание услуг
    """
    if not services:
        return 'У вас нет доступных услуг.'
    text = '*Список выполняемых Вами работ*\n\n'
    for service in services:
        text += f'-  {service.name}\n'
    return text


async def create_services_admin_text(services: list[Service]) -> str:
    """
    Формирует текстовое описание услуг
    :param services: список услуг
    :return: текстовое описание услуг
    """
    if not services:
        return 'Список услуг пуст.'
    text = '*Список услуг для выполнения подрядчиками*\n\n'
    for service in services:
        text += f'-  {service.name}\n'
    return text


async def text_service_admins(services: list[Service]) -> str:
    """
    Формирует текстовое описание услуг для администратора
    :param services: список услуг
    :return: текстовое описание услуг
    """
    if not services:
        return 'Услуги отсутствуют'
    text = '*Список услуг*\n\n'
    for service in services:
        text += f'-  {service.name}\n'
    return text


async def text_services_contr(services: list[Service]) -> str:
    """
    Текст для списка услуг
    :param services:
    :return:
    """
    if not services:
        return 'Услуги отсутствуют'
    text = ('*Выберите услугу*\n'
            '*Список услуг*\n\n')
    for service in services:
        text += f'-  {service.name}\n'
    return text


async def create_text_order(orders: list[Order]) -> str:
    """
    Текст для списка заказов для подрядчика
    :param orders: Список заказов
    :return:
    """
    text = '*Список выполненных заказов*\n\n'
    for order in orders:
        date = datetime.date.strftime(order.date, '%d-%m-%Y')
        service_name = order.service.name
        text += f'-  Тип работ - {service_name}  дата - {date}\n'
    return text


async def create_text_detail_order(order: Order) -> str:
    """
    Текст для подробного описания заказа
    :param order: Заказ
    :return:
    """
    date = datetime.date.strftime(order.date, '%d-%m-%Y')
    service_name = order.service.name

    text = (f'Заказ {order.id} {date}\n'
            f'Описание\n'
            f'{order.description}\n'
            f'Тип работ - {service_name}\n'
            f'Клиент - {order.client_name} {order.client_phone}')
    return text


async def create_text_statistic_users() -> str:
    today = datetime.datetime.today().date()
    all_users, users_with_date, top_5 = await asyncio.gather(ContractRepository.get_count_contractors(),
                                                             ContractRepository.get_contractors_date(today),
                                                             ContractRepository.get_top_5_contractors())
    text = (f'Общее количество подрядчиков: {all_users}\n'
            f'Подрядчики за сегодня: {users_with_date[0]}\n'
            f'Подрядчики за неделю: {users_with_date[1]}\n'
            f'Подрядчики за месяц: {users_with_date[2]}\n'
            f'Топ 5 подрядчиков по количеству заказов:\n')
    for contractor in top_5:
        username = contractor['user_name'].replace('_', '\_')
        text += f"@{username}. Количество заказов - {contractor['orders']}\n"
    return text


async def create_text_statistic_orders() -> str:
    today = datetime.datetime.today().date()
    orders_with_time, count_orders_by_type, top_services = \
        await asyncio.gather(OrderRepository.get_orders_date(today),
                             OrderRepository.get_count_orders(),
                             ServiceRepository.get_top_5_services())
    logger.info(top_services)
    text = (f'Количество активных заказов: {count_orders_by_type[0]}\n'
            f'Количество выполненных заказов: {count_orders_by_type[1]}\n'
            f'Заказов за сегодня: {orders_with_time[0]}\n'
            f'Заказов за неделю: {orders_with_time[1]}\n'
            f'Заказов за месяц: {orders_with_time[2]}\n'
            f'Топ 5 услуг по количеству заказов:\n')
    for service in top_services:
        text += f'{service["name"]}. Количество заказов - {service["order_count"]}\n'
    return text


async def create_exel_data_contractors():
    async for session in get_async_session():
        # 1. Запрос для получения данных о подрядчиках
        contractors_query = select(
                Contractors.id_telegram,
                Contractors.full_name,
                Contractors.number_phone,
                Contractors.user_name,
                Contractors.date_reg,
                Contractors.balance,
                Contractors.city,
                Contractors.company,
                Contractors.site,
                Contractors.social_media
        )
        contractors_result = await session.execute(contractors_query)
        contractors_data = contractors_result.fetchall()

        # 2. Запрос для подсчета активных и завершенных заказов
        orders_query = select(
                Order.user_telegram,
                func.count(case(
                        (Order.status == StatusEnum.active, Order.id),
                        else_=None
                )).label('active_orders'),
                func.count(case(
                        (Order.status == StatusEnum.completed, Order.id),
                        else_=None
                )).label('completed_orders')
        ).group_by(Order.user_telegram)

        orders_result = await session.execute(orders_query)
        orders_data = orders_result.fetchall()

        # 3. Запрос для получения услуг подрядчиков
        services_query = select(
                services_contractors.c.id_telegram,
                func.string_agg(Service.name, ', ').label('services')
        ).join(Service, Service.id == services_contractors.c.service_id) \
            .group_by(services_contractors.c.id_telegram)

        services_result = await session.execute(services_query)
        services_data = services_result.fetchall()

        # Преобразуем в удобные словари
        orders_dict = {order.user_telegram: order for order in orders_data}
        services_dict = {service.id_telegram: service.services for service in services_data}

        # 4. Объединяем все данные
        final_data = []
        for contractor in contractors_data:
            contractor_dict = {
                    'ID телеграм': contractor.id_telegram,
                    'ФИО': contractor.full_name,
                    'Номер телефона': contractor.number_phone,
                    'Город': contractor.city,
                    'Сайт': contractor.site,
                    'Компания': contractor.company,
                    'Соц.сети': contractor.social_media,
                    'Никнейм': contractor.user_name,
                    'Дата регистрации': contractor.date_reg,
                    'Баланс': contractor.balance,
                    'Активные заказы': 0,
                    'Выполненные заказы': 0,
                    'Услуги': services_dict.get(contractor.id_telegram, '')
            }

            # Заполняем количество активных и завершенных заказов
            if contractor.id_telegram in orders_dict:
                contractor_dict['Активные заказы'] = orders_dict[contractor.id_telegram].active_orders
                contractor_dict['Выполненные заказы'] = orders_dict[contractor.id_telegram].completed_orders

            final_data.append(contractor_dict)

        # Создаем DataFrame и сохраняем в Excel
        df = pd.DataFrame(final_data, columns=[
                'ID телеграм', 'ФИО', 'Номер телефона','Город', 'Сайт', 'Компания', 'Соц.сети',
                'Никнейм', 'Дата регистрации', 'Баланс',
                'Активные заказы', 'Выполненные заказы', 'Услуги'
        ])

        file_path = 'media/contractors_data.xlsx'
        if os.path.exists(file_path):
            os.remove(file_path)
        # Сохраняем данные в Excel
        df.to_excel(file_path, index=False)
        return file_path


async def create_exel_data_orders():
    async for session in get_async_session():
        query = (select(
                Order.date.label('Order Date'),
                Service.name.label('Service'),
                Order.client_name,
                Order.client_phone,
                Contractors.user_name.label('Username'),
                cast(Order.status, String).label('Status')
        )
                 .join(Service, Service.id == Order.service_id)  # Соединяем с таблицей услуг
                 .join(Contractors, Contractors.id_telegram == Order.user_telegram)  # Соединяем с подрядчиком
                 )

        result = await session.execute(query)
        data = result.fetchall()

        # Преобразуем результат в pandas DataFrame
        df = pd.DataFrame(data, columns=[
                'Дата заказа', 'Услуга', 'Имя клиента', 'Номер клиента', 'Исполнитель', 'Статус'
        ])
        file_path = 'media/orders_data.xlsx'
        if os.path.exists(file_path):
            os.remove(file_path)
        df.to_excel(file_path, index=False)
        return file_path
