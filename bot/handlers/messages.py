import asyncio
import datetime
import os
from sys import stdout
from unittest.mock import patch

from aiogram import Router, types, F
from pathlib import Path
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from pydantic_core._pydantic_core import ValidationError
from repositories import *
from utils.helpers import create_services_text, create_services_admin_text, text_services_contr
from .states import *
from keyboards import *
from utils import user_text, admin_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = Router()
list_admins = [5473168797, 718586333]
list_super_users = [718586333, 272513813]


@router.message(RegStates.FULL_NAME, F.content_type == 'text')
async def full_name_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки ввода ФИО подрядчика
    :param message:
    :param state:
    :return:
    """

    text = message.text
    if len(text.split()) != 3:
        await message.answer(
                "Не правильный ввод\n\n"
                "Пример ввода: Иванов Иван Иванович"
        )
        return
    user_id = message.from_user.id
    user_name = message.from_user.username
    if not user_name:
        await message.answer(
                "Для работы с ботом у вас должен иметься уникальный никнейм пользователя\n"
                "Зайдите в настройки аккаунта и создайте никнейм"
        )
        return
    await ContractRepository.create_contr(user_id, message.from_user.username, text)
    await state.set_state(RegStates.PHONE)
    await message.answer(
            user_text.phone_question,
            reply_markup=await contact_button()
    )


@router.message(RegStates.PHONE, F.content_type == 'text')
async def number_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки ввода номера телефона подрядчика
    :param message:
    :param state:
    :return:
    """
    text = message.text
    if len(text.split()) != 3:
        await message.answer(
                "Не правильный ввод\n\n"
                "Пример ввода: Иванов Иван Иванович"
        )
    user_id = message.from_user.id
    await ContractRepository.update_contractor(user_id, {"number_phone": text.strip()})
    await state.set_state(RegStates.CITY)
    await message.answer(
            user_text.city_question,
    )


@router.message(RegStates.CITY, F.content_type == 'text')
async def city_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки ввода города подрядчика
    :param message:
    :param state:
    :return:
    """
    text = message.text
    user_id = message.from_user.id
    await ContractRepository.update_contractor(user_id, {"city": text})
    await state.set_state(RegStates.COMPANY)
    await message.answer(
            user_text.company_question,
            reply_markup=pass_button
    )


@router.message(RegStates.COMPANY, F.content_type == 'text')
async def company_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки ввода города подрядчика
    :param message:
    :param state:
    :return:
    """
    text = message.text
    user_id = message.from_user.id
    await ContractRepository.update_contractor(user_id, {"company": text})
    await state.set_state(RegStates.SOCIAL)
    await message.answer(
            user_text.social_question,
            reply_markup=pass_button
    )


@router.message(RegStates.SOCIAL, F.content_type == 'text')
async def social_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки ввода ссылок на соц сети подрядчика
    :param message:
    :param state:
    :return:
    """
    text = message.text
    user_id = message.from_user.id
    await ContractRepository.update_contractor(user_id, {"social_media": text})
    await state.set_state(RegStates.SITE)
    await message.answer(
            user_text.site_question,
            reply_markup=pass_button
    )


@router.message(RegStates.SITE, F.content_type == 'text')
async def site_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки ввода сайта подрядчика
    :param message:
    :param state:
    :return:
    """
    text = message.text
    user_id = message.from_user.id
    await ContractRepository.update_contractor(user_id, {"site": text})
    await state.set_state(RegStates.SERVICE)
    services = await ServiceRepository.get_all_services()
    text = await text_services_contr(services)
    await message.answer(
            text,
            reply_markup=await list_services_menu(services),
            parse_mode='Markdown'
    )


@router.message(RegStates.PHONE, F.content_type == 'contact')
async def site_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки ввода сайта подрядчика
    :param message:
    :param state:
    :return:
    """
    phone_number = str(message.contact.phone_number)
    user_id = message.from_user.id
    await ContractRepository.update_contractor(user_id, {"number_phone": phone_number})
    await state.set_state(RegStates.CITY)
    await message.answer(
            user_text.city_question,
    )


@router.message(ServiceState.NAME_SERVICE, F.content_type == 'text')
async def add_service_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки ввода сайта подрядчика
    :param message:
    :param state:
    :return:
    """
    name = message.text
    await ServiceRepository.add_service_admin(name)
    await state.clear()
    await message.answer(
            f"Сервис - {name} добавлен!",
    )
    services = await ServiceRepository.get_all_services()
    text = await create_services_admin_text(services)
    await message.answer(
            text=text,
            parse_mode='Markdown',
            reply_markup=await admin_service_menu()
    )


@router.message(OrderCreateState.text_order, F.content_type == 'text')
async def text_order_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки ввода текста для составления заявки
    :param message:
    :param state:
    :return:
    """
    text = message.text
    order = await OrderRepository.create_order(text)
    await message.answer(
            admin_text.photo_order,
            reply_markup=await photo_finish_keyboard()
    )
    await state.update_data(order_id=order.id)
    await state.set_state(OrderCreateState.photo_order)


@router.message(OrderCreateState.photo_order, F.content_type.in_(['photo', 'document']))
async def files_order_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки отправки фотографий(файлов) для составления заявки
    :param message:
    :param state:
    :return:
    """
    media_folder = 'media'
    data = await state.get_data()
    order_id = data.get('order_id')
    prev_message = data.get('prev_message')
    path_files = ""
    date_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    if message.photo:
        photo = message.photo[-1]
        file_id = photo.file_id
        file_info = await message.bot.get_file(file_id)
        file_extension = file_info.file_path.split('.')[-1]
        file_path = os.path.join(media_folder, f"photo_{order_id}_{date_time}.{file_extension}")
        if file_path not in path_files:
            await message.bot.download_file(file_info.file_path, file_path)
            path_files += f"{file_path}\n"
    if message.document:
        doc = message.document
        file_id = doc.file_id
        file_info = await message.bot.get_file(file_id)
        file_extension = file_info.file_path.split('.')[-1]
        file_path = os.path.join(media_folder, f"document_{order_id}_{date_time}.{file_extension}")
        if file_path not in path_files:
            await message.bot.download_file(file_info.file_path, file_path)
            path_files += f"{file_path}\n"
    if not prev_message:
        order = await OrderRepository.update_photo_order(order_id, path_files)
        await state.update_data(prev_message=True)
    else:
        order = await OrderRepository.get_order_by_id(int(order_id))
        await OrderRepository.update_photo_order(order.id, order.photo_path + path_files)
    await message.delete()
    await message.answer(text="Фотография загружена!\n"
                              "Теперь отправьте следующую фотографию или нажмите кнопку 'Готово'")


@router.message(OrderCreateState.photo_order, F.text == "Готово")
async def files_order_ready(message: types.Message, state: FSMContext):
    data = await state.get_data()
    order_id = data.get('order_id')
    if order_id:
        text = admin_text.client_name
        await state.set_state(OrderCreateState.client_name_order)
        await message.answer(text)
        # services = await ServiceRepository.get_all_services()
        # await state.set_state(OrderCreateState.services_order)

        # text = "Выберите услугу для заказа\n\n"
        # text_2 = await create_services_admin_text(services)
        # keyboard = await add_service_in_order(services, int(order_id))
        # await message.answer(text=text + text_2,
        #                      reply_markup=keyboard, parse_mode="Markdown")


@router.message(OrderCreateState.client_name_order, F.content_type == 'text')
async def client_name_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки отправки имени клиента для заказа
    :param message:
    :param state:
    :return:
    """
    text = message.text
    data = await state.get_data()
    order_id = data.get('order_id')
    await OrderRepository.update_data_order(int(order_id), {'client_name': text})
    text = admin_text.client_phone
    await state.set_state(OrderCreateState.client_phone_order)
    await message.delete()
    await message.answer(
            text
    )


@router.message(OrderCreateState.client_phone_order, F.content_type == 'text')
async def client_phone_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки отправки номера клиента для заказа
    :param message:
    :param state:
    :return:
    """
    text = message.text
    data = await state.get_data()
    order_id = data.get('order_id')
    order, services = await asyncio.gather(
            OrderRepository.update_data_order(int(order_id), {'client_phone': text}),
            ServiceRepository.get_all_services())
    await state.set_state(OrderCreateState.services_order)
    text = "Выберите услугу для заказа\n\n"
    text_2 = await create_services_admin_text(services)
    keyboard = await add_service_in_order(services, int(order_id))
    await message.answer(text=text + text_2,
                         reply_markup=keyboard, parse_mode="Markdown")


@router.message(OrderCreateState.edit_text_order, F.content_type == 'text')
async def client_phone_processing(message: types.Message, state: FSMContext):
    """
    Функция обработки отправки номера клиента для заказа
    :param message:
    :param state:
    :return:
    """
    text = message.text
    data = await state.get_data()
    order_id = data.get('order_id')
    await message.delete()
    await OrderRepository.update_data_order(int(order_id), {'description': text})
    order = await OrderRepository.get_order_by_id(int(order_id))
    files_list = order.photo_path.split('\n')
    text = order.description + "\n\n" + f"Услуга - {order.service.name}"
    media_group = MediaGroupBuilder(caption=text)
    if order.photo_path:
        for path_file in files_list[:len(files_list) - 1]:
            if path_file:
                if files_list[0].split('.')[1].lower() in ['jpeg', 'png', 'jpg', 'svg', 'gif', 'raw', 'tiff']:
                    media = FSInputFile(path_file)
                    media_group.add_photo(media=media)
                else:
                    media = FSInputFile(path_file)
                    media_group.add_document(media=media)
        await message.answer_media_group(media=media_group.build())
    else:
        await message.answer(text)
    keyboard = await finish_order_keyboard(order.id)
    await message.answer("Создать заказ и оповестить подрядчиков?", reply_markup=keyboard)
    await state.clear()


@router.message(F.text == "Назад")
async def callback_unlock(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    if user_id in list_admins:
        await message.answer(admin_text.text_start, reply_markup=await main_menu_admin())
    elif user_id in list_super_users:
        await message.answer(admin_text.super_admin_text, reply_markup=await super_admin_menu())


@router.message(F.text == "Статистика")
async def files_order_ready(message: types.Message, state: FSMContext):
    if message.from_user.id not in list_super_users:
        return
    text = "Выберите нужный вид статистики"
    keyboard = await statistic_menu()
    await message.answer(text, reply_markup=keyboard)


@router.message(F.text == "Заблокировать подрядчика")
async def callback_block(message: types.Message, state: FSMContext):
    if message.from_user.id not in list_super_users:
        return
    text = "Отправьте никнейм подрядчика, которого необходимо заблокировать"
    await state.set_state(AdminStates.NAME_USER_BLOCK)
    await message.answer(text, reply_markup=back_reply_but)


@router.message(F.text == "Разблокировать подрядчика")
async def callback_unlock(message: types.Message, state: FSMContext):
    if message.from_user.id not in list_super_users:
        return
    text = "Отправьте никнейм подрядчика, которого необходимо разблокировать"
    await state.set_state(AdminStates.NAME_USER_UNLOCK)
    await message.answer(text, reply_markup=back_reply_but)


@router.message(AdminStates.NAME_USER_BLOCK, F.content_type == 'text')
async def user_block_processing(message: types.Message, state: FSMContext):
    contractor = await ContractRepository.get_user_by_name(message.text)
    if not contractor:
        await message.answer("Пользователь с таким никнеймом не найден\n"
                             "Попробуйте ещё раз, или нажмите кнопку Назад",
                             reply_markup=back_reply_but)
        return
    await ContractRepository.update_contractor(contractor.id_telegram, {'active': False})
    await state.set_state(None)
    await message.answer(f"Подрядчик заблокирован", reply_markup=back_reply_but)
    await message.bot.send_message(contractor.id_telegram, text="Вы были заблокированы администратором")


@router.message(AdminStates.NAME_USER_UNLOCK, F.content_type == 'text')
async def user_unlock_processing(message: types.Message, state: FSMContext):
    contractor = await ContractRepository.get_user_by_name(message.text)
    if not contractor:
        await message.answer("Пользователь с таким никнеймом не найден\n"
                             "Попробуйте ещё раз, или нажмите кнопку Назад",
                             reply_markup=back_reply_but)
        return
    await ContractRepository.update_contractor(contractor.id_telegram, {'active': True})
    await state.set_state(None)
    await message.answer("Подрядчик разблокирован", reply_markup=back_reply_but)
