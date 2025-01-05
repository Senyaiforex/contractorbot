import datetime

from models import Service, Order


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