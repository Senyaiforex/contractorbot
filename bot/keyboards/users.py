from aiofiles import stdout
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
import datetime
from models import Service, Order
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main_menu_contractors(registration: True) -> InlineKeyboardMarkup:
    """
    Функция создаёт кнопки для меню подрядчиков
    :return: InlineKeyboardMarkup
    """
    if registration:
        return InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='📃 Мои услуги', callback_data='my_services')],
                [InlineKeyboardButton(text='💵 Пополнить баланс', callback_data='up_balance')],
                [InlineKeyboardButton(text='🔗 Мои заказы', callback_data='my_orders')],
                [InlineKeyboardButton(text='🆘 Поддержка', url="https://t.me/BH_help")]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='📋 Регистрация', callback_data='registration')],
        ])


async def services_menu() -> InlineKeyboardMarkup:
    """
    Функция создаёт кнопки для меню подрядчиков
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='➕ Добавить услугу', callback_data='service_add')],
            [InlineKeyboardButton(text='➖ Удалить услугу', callback_data='service_del')],
            [InlineKeyboardButton(text='🔙 Назад', callback_data='menu')],
    ])


async def up_balance_vars() -> InlineKeyboardMarkup:
    """
    Функция создаёт кнопки для выбора на сколько пополнить баланс
    :return: InlineKeyboardMarkup
    """
    list_balance = [500, 1000, 1500, 2000, 2500, 3000]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for price in list_balance:
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=f"{price} р.", callback_data=f"pay_{price}")])
    keyboard.inline_keyboard.append([InlineKeyboardButton(text='🔙 Назад', callback_data='menu')])
    return keyboard


async def list_services_menu(services: list[Service]):
    """
    Функция создаёт список услуг в виде инлайн кнопок
    :param services:
    :return:
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for index in range(0, len(services) + 1, 3):
        if index + 1 == len(services):
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"adding_service_{services[index].id}"),
                                             InlineKeyboardButton(text='✔️ Готово', callback_data='ready_reg')
                                             ])
        elif index + 2 == len(services):
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"adding_service_{services[index].id}"),
                                             InlineKeyboardButton(text=services[index + 1].name,
                                                                  callback_data=f"adding_service_{services[index + 1].id}"),
                                             InlineKeyboardButton(text='✔️ Готово', callback_data='ready_reg')])
        elif index == len(services) - 1:
            keyboard.inline_keyboard.append([(InlineKeyboardButton(text='✔️ Готово', callback_data='ready_reg'))])
        elif index >= len(services):
            keyboard.inline_keyboard.append([(InlineKeyboardButton(text='✔️ Готово', callback_data='ready_reg'))])
        else:
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"adding_service_{services[index].id}"),
                                             InlineKeyboardButton(text=services[index + 1].name,
                                                                  callback_data=f"adding_service_{services[index + 1].id}"),
                                             InlineKeyboardButton(text=services[index + 2].name,
                                                                  callback_data=f"adding_service_{services[index + 2].id}")])
    return keyboard


async def add_service_keyboard(services: list[Service]):
    """
    Функция создаёт список услуг в виде инлайн кнопок
    :param services:
    :return:
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for index in range(0, len(services) + 1, 3):
        if index + 1 == len(services):
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"add-new-service_{services[index].id}"),
                                             InlineKeyboardButton(text='✔️ Готово', callback_data='my_services')
                                             ])
        elif index + 2 == len(services):
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"add-new-service_{services[index].id}"),
                                             InlineKeyboardButton(text=services[index + 1].name,
                                                                  callback_data=f"add-new-service_{services[index + 1].id}"),
                                             InlineKeyboardButton(text='✔️ Готово', callback_data='my_services')])
        elif index == len(services) - 1:
            keyboard.inline_keyboard.append([(InlineKeyboardButton(text='✔️ Готово', callback_data='my_services'))])
        elif index >= len(services):
            keyboard.inline_keyboard.append([(InlineKeyboardButton(text='✔️ Готово', callback_data='my_services'))])
        else:
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"add-new-service_{services[index].id}"),
                                             InlineKeyboardButton(text=services[index + 1].name,
                                                                  callback_data=f"add-new-service_{services[index + 1].id}"),
                                             InlineKeyboardButton(text=services[index + 2].name,
                                                                  callback_data=f"add-new-service_{services[index + 2].id}")])
    return keyboard


async def delete_service_keyboard(services: list[Service]):
    """
    Функция создаёт список услуг в виде инлайн кнопок
    :param services:
    :return:
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for index in range(0, len(services) + 1, 3):
        if index + 1 == len(services):
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"delete-service_{services[index].id}"),
                                             InlineKeyboardButton(text='✔️ Готово', callback_data='my_services')
                                             ])
        elif index + 2 == len(services):
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"delete-service_{services[index].id}"),
                                             InlineKeyboardButton(text=services[index + 1].name,
                                                                  callback_data=f"delete-service_{services[index + 1].id}"),
                                             InlineKeyboardButton(text='✔️ Готово', callback_data='my_services')])
        elif index == len(services) - 1:
            keyboard.inline_keyboard.append([(InlineKeyboardButton(text='✔️ Готово', callback_data='my_services'))])
        elif index >= len(services):
            keyboard.inline_keyboard.append([(InlineKeyboardButton(text='✔️ Готово', callback_data='my_services'))])
        else:
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"delete-service_{services[index].id}"),
                                             InlineKeyboardButton(text=services[index + 1].name,
                                                                  callback_data=f"delete-service_{services[index + 1].id}"),
                                             InlineKeyboardButton(text=services[index + 2].name,
                                                                  callback_data=f"delete-service_{services[index + 2].id}")])
    return keyboard


async def contact_button():
    """
    Функция создаёт кнопку для отправки номера телефона
    :return:
    """
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Поделиться номером", request_contact=True,
                                                             )]], resize_keyboard=True, one_time_keyboard=True)
    return keyboard


async def offer_order(user_id: int, order_id: int):
    """
    Функция создаёт кнопку для предложения взять заказ
    :return:
    """
    but_yes = [InlineKeyboardButton(text="Взять заказ в работу", callback_data=f"yes-offer-order_{user_id}_{order_id}")]
    but_no = [InlineKeyboardButton(text="Отказаться", callback_data=f"no-offer-order")]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[but_yes, but_no])
    return keyboard


async def after_order_keyboard():
    """
    Функция создаёт кнопку для предложения взять заказ
    :return:
    """
    return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='💵 Пополнить баланс', callback_data='up_balance')],
            [InlineKeyboardButton(text='🔙 Меню', callback_data='menu')],
    ])


async def payment_keyboard(url):
    """
    Функция создаёт кнопку для оплаты заказа
    :return:
    """
    return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Оплатить заказ', url=url)],
            [InlineKeyboardButton(text='Назад', callback_data='menu')]])


async def orders_keyboard():
    """
    Функция создаёт инлайн кнопки для просмотра заказов
    :return:
    """
    but_1 = [InlineKeyboardButton(text="Активные заказы", callback_data="active_orders")]
    but_2 = [InlineKeyboardButton(text="Выполненные заказы", callback_data="completed_orders")]
    back_but = [InlineKeyboardButton(text='Назад', callback_data='menu')]

    return InlineKeyboardMarkup(inline_keyboard=[but_1, but_2, back_but])


async def orders_select_keyboard(orders: list[Order]) -> InlineKeyboardMarkup:
    """
    Функция создаёт инлайн кнопки для заказов для перехода в заказ
    :param orders:
    :return:
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for order in orders:
        text = datetime.date.strftime(order.date, '%d-%m-%Y')
        keyboard.inline_keyboard.append([InlineKeyboardButton(text=text,
                                                              callback_data=f"detail_order_{order.id}")])
    keyboard.inline_keyboard.append([InlineKeyboardButton(text='Назад', callback_data='my_orders')])
    return keyboard

async def order_detail_keyboard(order_id: int, type_order: str) -> InlineKeyboardMarkup:
    """
    Функция создаёт инлайн кнопки для заказа
    :param type_order:
    :return:
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    if type_order == 'active':
        but_1 = [InlineKeyboardButton(text='✅ Выполнен', callback_data=f'order-status-edit_{order_id}')]
        but_2 = [InlineKeyboardButton(text='Назад', callback_data="active_orders")]
        but_3 = [InlineKeyboardButton(text='Меню', callback_data="menu")]
        keyboard.inline_keyboard.append(but_1)
        keyboard.inline_keyboard.append(but_2)
        keyboard.inline_keyboard.append(but_3)
    else:
        but_2 = [InlineKeyboardButton(text='Назад', callback_data="completed_orders")]
        but_3 = [InlineKeyboardButton(text='Меню', callback_data="menu")]
        keyboard.inline_keyboard.append(but_2)
        keyboard.inline_keyboard.append(but_3)
    return keyboard


pass_button = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Пропустить")]],
                                  one_time_keyboard=True,
                                  resize_keyboard=True,
                                  is_persistent=False)
menu_button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='В меню', callback_data='menu')]])