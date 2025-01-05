import asyncio
from contextlib import suppress
import os
from pathlib import Path

from aiogram.utils.media_group import MediaGroupBuilder
from models import StatusEnum
from handlers.states import RegStates, ServiceState, OrderCreateState
from utils import admin_text, user_text
from utils.helpers import create_services_text, text_service_admins, create_services_admin_text, text_services_contr, \
    create_text_order, create_text_detail_order
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, InputMediaDocument, InputFile
from keyboards import main_menu_admin, main_menu_contractors, services_menu, up_balance_vars, list_services_menu, \
    add_service_keyboard, delete_service_keyboard, admin_service_menu, delete_service_admin, back_but, \
    finish_order_keyboard, offer_order, after_order_keyboard, payment_keyboard, orders_keyboard, order_detail_keyboard, \
    orders_select_keyboard
from repositories import ServiceRepository, ContractRepository, OrderRepository
from utils.payment import create_url_payment
import logging

list_admins = [272513813]
router = Router()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.callback_query(lambda c: c.data == 'menu')
async def main_menu(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Меню»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    await state.clear()
    user_id = callback_query.from_user.id
    if user_id in list_admins:
        await callback_query.message.edit_text(text=admin_text.text_start,
                                               reply_markup=await main_menu_admin())
    else:
        contractor = await ContractRepository.get_contractor_by_id(user_id)
        reg = True if contractor else False
        text = user_text.text_start if not reg else user_text.text_constr.format(fio=contractor.full_name,
                                                                                 balance=contractor.balance,
                                                                                 number=contractor.number_phone,
                                                                                 city=contractor.city)
        await callback_query.message.edit_text(text=text,
                                               reply_markup=await main_menu_contractors(reg))


@router.callback_query(lambda c: c.data == 'registration')
async def registration(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Регистрация»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    await callback_query.message.delete()
    text = user_text.fio_question
    await callback_query.message.answer(
            text=text,
            parse_mode='Markdown'
    )
    await state.set_state(RegStates.FULL_NAME)


@router.callback_query(lambda c: c.data == 'my_services')
async def my_services(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Мои услуги»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    user_id = callback_query.from_user.id
    services = await ServiceRepository.get_services_by_contractor(user_id)
    text = await create_services_text(services)
    await callback_query.message.edit_text(
            text=text,
            parse_mode='Markdown',
            reply_markup=await services_menu()
    )


@router.callback_query(lambda c: c.data == 'list_services')
async def my_services(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Список услуг»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    services = await ServiceRepository.get_all_services()
    text = await create_services_admin_text(services)
    await callback_query.message.edit_text(
            text=text,
            parse_mode='Markdown',
            reply_markup=await admin_service_menu()
    )


@router.callback_query(lambda c: c.data == 'my_orders')
async def my_orders(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Мои заказы»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    orders = await OrderRepository.get_orders_by_user(callback_query.from_user.id, 'all')
    if not orders:
        await callback_query.answer("Список заказов пуст")
        return
    text = "Выберите нужный тип заказа"
    keyboard = await orders_keyboard()
    await callback_query.message.edit_text(
            text=text,
            parse_mode='Markdown',
            reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data == 'up_balance')
async def up_balance(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Пополнить баланс»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    await callback_query.message.edit_text(
            text="Выберите сумму для пополнения 💵",
            parse_mode='Markdown',
            reply_markup=await up_balance_vars()
    )


@router.callback_query(lambda c: c.data.startswith('pay_'))
async def payment_callback(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку при выборе суммы пополнения баланса
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    price = float(callback_query.data.split('_')[1])
    await callback_query.message.delete()
    link_pay = await create_url_payment(callback_query.from_user.id, 20)
    keyboard = await payment_keyboard(link_pay)
    await callback_query.message.answer(
            text="Перейдите по ссылке и пополните свой баланс.\n"
                 "После покупки мы оповестим Вас, что баланс пополнен",
            parse_mode='Markdown',
            reply_markup=keyboard
    )


# @router.callback_query(lambda c: c.data.startswith('service_'))
# async def services_processing(callback_query: CallbackQuery, state: FSMContext):
#     """
#     Функция обработки нажатия на inline-кнопку «Добавить услугу» или «Удалить услугу»
#     :param callback_query: CallbackQuery
#     :param state: FSMContext
#     :return:
#     """
#     dict_actions = {'add': "Введите название вида работ для добавления",
#                     'del': "Выберите вид работ для удаления"}
#     type_action = callback_query.data.split('_')[1]
#     text = dict_actions[type_action]
#     await callback_query.message.delete()
#     if type_action == 'add':
#         await callback_query.message.answer(
#                 text=text,
#                 parse_mode='Markdown',
#         )
#     else:
#         await callback_query.message.answer(
#                 text="Выберите вид работ для удаления",
#                 parse_mode='Markdown',
#                 reply_markup=await services_menu()
#         )


@router.callback_query(lambda c: c.data.startswith('adding_service_'))
async def services_add_processing(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку при выборе типа оказываемых услуг при регистрации подрядчика
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    id_service = callback_query.data.split('_')[2]
    service, user, services = await asyncio.gather(ServiceRepository.get_service_by_id(int(id_service)),
                                                   ContractRepository.add_service(callback_query.from_user.id,
                                                                                  int(id_service)),
                                                   ServiceRepository.get_all_services())
    await callback_query.answer(f"Услуга {service.name} добавлена")
    services_user = await ServiceRepository.get_services_by_contractor(callback_query.from_user.id)
    services_user = [service.id for service in services_user]
    services = [service_req for service_req in services if service_req.id not in services_user]
    text = await text_services_contr(services)
    keyboard = await list_services_menu(services)
    await callback_query.message.edit_text(text=text, reply_markup=keyboard, parse_mode='Markdown')


@router.callback_query(lambda c: c.data.startswith('ready_reg'))
async def end_registration(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку Готово при окончании регистрации
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    text = user_text.reg_finish
    await state.clear()
    await callback_query.message.edit_text(text,
                                           reply_markup=await main_menu_contractors(True),
                                           parse_mode='Markdown')


@router.callback_query(lambda c: c.data.startswith('service_add'))
async def service_add_processing(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку Готово при окончании регистрации
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    service_user, services = await asyncio.gather(
            ServiceRepository.get_services_by_contractor(callback_query.from_user.id),
            ServiceRepository.get_all_services())
    services_user = [service.id for service in service_user]
    services = [service_req for service_req in services if service_req.id not in services_user]
    text = await text_services_contr(services)
    await callback_query.message.edit_text(text, reply_markup=await add_service_keyboard(services),
                                           parse_mode='Markdown')


@router.callback_query(lambda c: c.data.startswith('add-new-service'))
async def service_add_new(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку Готово при окончании регистрации
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    id_service = callback_query.data.split('_')[1]
    service, user = await asyncio.gather(ServiceRepository.get_service_by_id(int(id_service)),
                                         ContractRepository.add_service(callback_query.from_user.id,
                                                                        int(id_service)))
    await callback_query.answer(f"Услуга {service.name} добавлена")
    service_user, services = await asyncio.gather(
            ServiceRepository.get_services_by_contractor(callback_query.from_user.id),
            ServiceRepository.get_all_services())
    services_user = [service.id for service in service_user]
    services = [service_req for service_req in services if service_req.id not in services_user]
    text = await text_services_contr(services)
    await callback_query.message.edit_text(text=text, reply_markup=await add_service_keyboard(services),
                                           parse_mode='Markdown')


@router.callback_query(lambda c: c.data.startswith('service_del'))
async def service_del_processing(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку Готово при окончании регистрации
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    service_user = await ServiceRepository.get_services_by_contractor(callback_query.from_user.id)
    text = await text_services_contr(service_user)
    await callback_query.message.edit_text(text, reply_markup=await delete_service_keyboard(service_user),
                                           parse_mode='Markdown')


@router.callback_query(lambda c: c.data.startswith('delete-service'))
async def service_del_old(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку Готово при окончании регистрации
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    id_service = callback_query.data.split('_')[1]
    service, user = await asyncio.gather(ServiceRepository.get_service_by_id(int(id_service)),
                                         ContractRepository.del_service(callback_query.from_user.id,
                                                                        int(id_service)))
    await callback_query.answer(f"Услуга {service.name} удалена")
    service_user = await ServiceRepository.get_services_by_contractor(callback_query.from_user.id)
    text = await text_services_contr(service_user)
    await callback_query.message.edit_text(text=text, reply_markup=await delete_service_keyboard(service_user),
                                           parse_mode='Markdown')


@router.callback_query(lambda c: c.data == 'delete_service')
async def service_del_admin_processing(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку Готово при окончании регистрации
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    services = await ServiceRepository.get_all_services()
    text = await text_services_contr(services)
    await callback_query.message.edit_text(text, reply_markup=await delete_service_admin(services),
                                           parse_mode='Markdown')


@router.callback_query(lambda c: c.data == 'update_service')
async def service_add_admin_processing(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку Готово при окончании регистрации
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    await callback_query.message.delete()
    text = "Введите название услуги"
    await callback_query.message.answer(text)
    await state.set_state(ServiceState.NAME_SERVICE)


@router.callback_query(lambda c: c.data.startswith('admin-delete-service'))
async def service_admin_delete(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку Готово при окончании регистрации
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    id_service = callback_query.data.split('_')[1]
    service = await ServiceRepository.get_service_by_id(int(id_service))
    await ServiceRepository.del_service_admin(int(id_service))
    services = await ServiceRepository.get_all_services()
    text = await text_services_contr(services)
    await callback_query.answer(f"Услуга {service.name} удалена")
    await callback_query.message.edit_text(text=text, reply_markup=await delete_service_admin(services),
                                           parse_mode='Markdown')


@router.callback_query(lambda c: c.data.startswith('add_order'))
async def add_order(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Разместить заказ»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    await callback_query.message.delete()
    text = admin_text.name_order
    await callback_query.message.answer(text)
    await state.set_state(OrderCreateState.text_order)


@router.callback_query(lambda c: c.data.startswith('add-in-order'))
async def add_service_in_order(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Добавить услугу в заказ»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    _, order_id, service_id = callback_query.data.split('_')
    await callback_query.message.delete()
    await OrderRepository.add_service_to_order(int(order_id), int(service_id))
    order = await OrderRepository.get_order_by_id(int(order_id))
    text = order.description + "\n\n" + f"Услуга - {order.service.name}"
    media_group = MediaGroupBuilder(caption=text)
    if order.photo_path:
        files_list = order.photo_path.split('\n')
        for path_file in files_list[:len(files_list) - 1]:
            if path_file:
                if files_list[0].split('.')[1].lower() in ['jpeg', 'png', 'jpg', 'svg', 'gif', 'raw', 'tiff']:
                    media = FSInputFile(path_file)
                    media_group.add_photo(media=media)
                else:
                    media = FSInputFile(path_file)
                    media_group.add_document(media=media)
        await callback_query.message.answer_media_group(media=media_group.build())
    else:
        await callback_query.message.answer(text)
    keyboard = await finish_order_keyboard(order.id)
    await callback_query.message.answer("Создать заказ и оповестить подрядчиков?", reply_markup=keyboard)
    await state.clear()


@router.callback_query(lambda c: c.data.startswith('edit_text'))
async def text_in_order_change(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку 'Отредактировать текст'
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    id_order = int(callback_query.data.split('_')[2])
    await state.update_data(order_id=id_order)
    text = "Отправьте текст для заказа"
    await callback_query.message.delete()
    await callback_query.message.answer(text)
    await state.set_state(OrderCreateState.edit_text_order)


@router.callback_query(lambda c: c.data.startswith('finish_order_'))
async def finish_create_order(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Создать заказ»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    order_id = callback_query.data.split('_')[2]
    order = await OrderRepository.get_order_by_id(int(order_id))
    text = order.description + "\n\n" + f"Услуга - {order.service.name}"
    media_group = MediaGroupBuilder(caption=text)
    await callback_query.message.delete_reply_markup()
    if order.photo_path:
        files_list = order.photo_path.split('\n')
        for path_file in files_list[:len(files_list) - 1]:
            if path_file:
                if files_list[0].split('.')[1].lower() in ['jpeg', 'png', 'jpg', 'svg', 'gif', 'raw', 'tiff']:
                    media = FSInputFile(path_file)
                    media_group.add_photo(media=media)
                else:
                    media = FSInputFile(path_file)
                    media_group.add_document(media=media)
    await callback_query.message.answer("Заказ создан. Все подрядчики будут оповещены", reply_markup=back_but)
    contractors = await ContractRepository.get_contractors_for_order(order.service.id)
    await state.clear()
    for contractor in contractors:
        keyboard = await offer_order(contractor.id_telegram, order.id)
        text_for_user = user_text.text_order if not contractor.free_try else user_text.text_order_try
        if order.photo_path:
            await callback_query.bot.send_media_group(contractor.id_telegram, media=media_group.build())
            await callback_query.bot.send_message(chat_id=contractor.id_telegram,
                                                  text=text_for_user,
                                                  reply_markup=keyboard,
                                                  parse_mode='Markdown')
        else:
            await callback_query.bot.send_message(chat_id=contractor.id_telegram,
                                                  text=text)
            await callback_query.bot.send_message(chat_id=contractor.id_telegram,
                                                  text=text_for_user,
                                                  reply_markup=keyboard,
                                                  parse_mode='Markdown')


@router.callback_query(lambda c: c.data.startswith('yes-offer-order'))
async def yes_order_offer(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Взять заказ в работу»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    _, user_id, order_id = callback_query.data.split('_')
    order, user = await asyncio.gather(OrderRepository.get_order_by_id(int(order_id)),
                                       ContractRepository.get_contractor_by_id(int(user_id)))
    await callback_query.message.delete_reply_markup()
    if order.user_telegram:
        await callback_query.message.edit_text(text="Заказ взял другой подрядчик\n\n"
                                                    "В следующий раз старайтесь реагировать на заказ быстрее",
                                               reply_markup=back_but)
        return
    if user.free_try:
        await callback_query.message.answer("Вы взяли пробный заказ!\n"
                                            "В следующий раз взять заказ в работу будет стоить 100р.\n"
                                            "Не забудьте пополнить баланс, иначе Вам не будут приходить оповещения о заказах!\n\n"
                                            "Для выполнения заказа свяжитесь с клиентом:\n"
                                            f"Номер телефона {order.client_phone}, Имя - {order.client_name}",
                                            reply_markup=await after_order_keyboard())
        await ContractRepository.update_contractor(callback_query.from_user.id, {"free_try": False})
    else:
        await ContractRepository.decrease_balance(callback_query.from_user.id, 100)
        await callback_query.message.answer("Вы взяли заказ!\n"
                                            "С Вашего баланса списано 100р.\n\n"
                                            "Для выполнения заказа свяжитесь с клиентом:\n"
                                            f"Номер телефона {order.client_phone}, Имя - {order.client_name}",
                                            reply_markup=await after_order_keyboard())
    await OrderRepository.add_user_in_order(order.id, user.id_telegram)

    for manager_id in list_admins:
        text = (f"*{user.full_name}* @{user.user_name} подтвердил заявку на выполнение работ\n\n"
                f"{order.description}\n\n"
                f"Услуга - {order.service.name}")
        await callback_query.bot.send_message(chat_id=manager_id, text=text, parse_mode="Markdown")


@router.callback_query(lambda c: c.data.startswith('no-offer-order'))
async def yes_order_offer(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Взять заказ в работу»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    await callback_query.message.delete_reply_markup()
    await callback_query.message.edit_text(text="Вы отказались от выполнения заказа\n\n"
                                                "Скоро будут следующие заказы, не пропустите! Вдруг они Вам подойдут",
                                           reply_markup=back_but)
    return


@router.callback_query(lambda c: c.data == 'active_orders')
async def my_active_orders(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Активные заказы»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    orders = await OrderRepository.get_orders_by_user(callback_query.from_user.id,
                                                      'active')
    if not orders:
        await callback_query.answer("Список активных заказов пуст")
        return
    text = "Список активных заказов"
    keyboard = await orders_select_keyboard(orders)
    await callback_query.message.edit_text(
            text=text,
            parse_mode='Markdown',
            reply_markup=keyboard
    )

@router.callback_query(lambda c: c.data == 'completed_orders')
async def my_completed_orders(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Выполненные заказы»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    orders = await OrderRepository.get_orders_by_user(callback_query.from_user.id,
                                                      'completed')
    if not orders:
        await callback_query.answer("Список выполненных заказов пуст")
        return
    text = "Список выполненных заказов"
    keyboard = await orders_select_keyboard(orders)
    await callback_query.message.edit_text(
            text=text,
            parse_mode='Markdown',
            reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data.startswith('detail_order_'))
async def detail_order(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «Заказ»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    order_id = int(callback_query.data.split('_')[2])
    order = await OrderRepository.get_order_by_id(int(order_id))
    text = await create_text_detail_order(order)
    keyboard = await order_detail_keyboard(order_id, order.status.name)
    await callback_query.message.edit_text(
            text=text,
            parse_mode='Markdown',
            reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data.startswith('order-status-edit'))
async def change_status_order(callback_query: CallbackQuery, state: FSMContext):
    """
    Функция обработки нажатия на inline-кнопку «✅ Выполнен»
    :param callback_query: CallbackQuery
    :param state: FSMContext
    :return:
    """
    order_id = int(callback_query.data.split('_')[1])
    await callback_query.answer("Статус заказа изменён")
    await OrderRepository.update_data_order(order_id, {"status": StatusEnum.completed})
    await my_completed_orders(callback_query, state)