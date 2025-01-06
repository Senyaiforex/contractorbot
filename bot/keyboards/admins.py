from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)

from models import Service


async def main_menu_admin() -> InlineKeyboardMarkup:
    """
    Функция создаёт кнопки для меню администратора
    :return: InlineKeyboardMarkup
    """

    return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='📃 Список услуг', callback_data='list_services')],
            [InlineKeyboardButton(text='➕ Разместить заказ', callback_data='add_order')],
            [InlineKeyboardButton(text='❌ Заблокировать подрядчика', callback_data='user_block')],
            [InlineKeyboardButton(text='✅ Разблокировать подрядчика', callback_data='user_unlock')]
    ])


async def admin_service_menu():
    """
    Функция создаёт кнопки для меню администратора услуг
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Добавить услугу', callback_data='update_service')],
            [InlineKeyboardButton(text='Удалить услугу', callback_data='delete_service')],
            [InlineKeyboardButton(text='🔙 Назад', callback_data='menu')]
    ])


async def delete_service_admin(services: list[Service]):
    """
    Функция создаёт список услуг в виде инлайн кнопок
    :param services:
    :return:
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for index in range(0, len(services) + 1, 3):
        if index + 1 == len(services):
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"admin-delete-service_{services[index].id}"),
                                             InlineKeyboardButton(text='✔️ Готово', callback_data='list_services')
                                             ])
        elif index + 2 == len(services):
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"admin-delete-service_{services[index].id}"),
                                             InlineKeyboardButton(text=services[index + 1].name,
                                                                  callback_data=f"admin-delete-service_{services[index + 1].id}"),
                                             InlineKeyboardButton(text='✔️ Готово', callback_data='list_services')])
        elif index == len(services) - 1:
            keyboard.inline_keyboard.append([(InlineKeyboardButton(text='✔️ Готово', callback_data='list_services'))])
        elif index >= len(services):
            keyboard.inline_keyboard.append([(InlineKeyboardButton(text='✔️ Готово', callback_data='list_services'))])
        else:
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"admin-delete-service_{services[index].id}"),
                                             InlineKeyboardButton(text=services[index + 1].name,
                                                                  callback_data=f"admin-delete-service_{services[index + 1].id}"),
                                             InlineKeyboardButton(text=services[index + 2].name,
                                                                  callback_data=f"admin-delete-service_{services[index + 2].id}")])
    return keyboard


async def add_service_in_order(services: list[Service], order_id: int):
    """
    Функция создаёт список услуг в виде инлайн кнопок
    :param services:
    :return:
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for index in range(0, len(services) + 1, 3):
        if index + 1 == len(services):
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"add-in-order_{order_id}_{services[index].id}"),
                                             InlineKeyboardButton(text='✔️ Готово', callback_data='create_order')
                                             ])
        elif index + 2 == len(services):
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"add-in-order_{order_id}_{services[index].id}"),
                                             InlineKeyboardButton(text=services[index + 1].name,
                                                                  callback_data=f"add-in-order_{order_id}_{services[index + 1].id}"),
                                             InlineKeyboardButton(text='✔️ Готово', callback_data='create_order')])
        elif index == len(services) - 1:
            keyboard.inline_keyboard.append([(InlineKeyboardButton(text='✔️ Готово', callback_data='create_order'))])
        elif index >= len(services):
            keyboard.inline_keyboard.append([(InlineKeyboardButton(text='✔️ Готово', callback_data='create_order'))])
        else:
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=services[index].name,
                                                                  callback_data=f"add-in-order_{order_id}_{services[index].id}"),
                                             InlineKeyboardButton(text=services[index + 1].name,
                                                                  callback_data=f"add-in-order_{order_id}_{services[index + 1].id}"),
                                             InlineKeyboardButton(text=services[index + 2].name,
                                                                  callback_data=f"add-in-order_{order_id}_{services[index + 2].id}")])
    return keyboard


async def finish_order_keyboard(order_id: int):
    """
    Функция создаёт кнопку для завершения заказа
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Создать заказ',
                                                                       callback_data=f"finish_order_{order_id}")],
                                                 [InlineKeyboardButton(text='Отредактировать текст',
                                                                       callback_data=f"edit_text_{order_id}")],
                                                 [InlineKeyboardButton(text='Назад',
                                                                       callback_data="menu")]])


async def photo_finish_keyboard():
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Готово")]],
                                   one_time_keyboard=True,
                                   resize_keyboard=True,
                                   is_persistent=False)
    return keyboard


async def super_admin_menu() -> ReplyKeyboardMarkup:
    """
    Функция создаёт инлайн кнопки для меню администратора
    :return:
    """
    but_1 = [KeyboardButton(text='Статистика')]
    but_2 = [KeyboardButton(text='Заблокировать подрядчика')]
    but_3 = [KeyboardButton(text='Разблокировать подрядчика')]
    return ReplyKeyboardMarkup(keyboard=[but_1, but_2, but_3],
                               one_time_keyboard=False,
                               resize_keyboard=True,
                               is_persistent=True)

async def statistic_menu() -> InlineKeyboardMarkup:
    """
    Функция создаёт инлайн кнопки для меню статистики
    :return:
    """
    but_1 = [InlineKeyboardButton(text='Статистика по заказам', callback_data='statistic_orders')]
    but_2 = [InlineKeyboardButton(text='Статистика по подрядчикам', callback_data='statistic_users')]
    but_3 = [InlineKeyboardButton(text='Выгрузить данные в exel', callback_data='exel_download')]
    return InlineKeyboardMarkup(inline_keyboard=[but_1, but_2, but_3])


back_reply_but = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Назад")]],
                                     one_time_keyboard=True,
                                     resize_keyboard=True,
                                     is_persistent=False)
back_but = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔙 Назад', callback_data='menu')]])
