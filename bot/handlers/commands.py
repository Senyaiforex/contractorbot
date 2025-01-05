import logging

from aiogram.fsm.context import FSMContext

from utils import user_text, admin_text
from aiogram import Router, types
from aiogram.filters import Command
from keyboards import main_menu_admin, main_menu_contractors
from repositories import ContractRepository

router = Router()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
list_admins = [272513813]


@router.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    """
    Основная функция для начала работы с ботом
    :param message:
    :return:
    """
    await state.clear()
    user_id = message.from_user.id
    if user_id in list_admins:
        await message.answer(admin_text.text_start, reply_markup=await main_menu_admin())
    else:
        contractor = await ContractRepository.get_contractor_by_id(user_id)
        reg = True if contractor else False
        text = user_text.text_start if not reg else user_text.text_constr.format(fio=contractor.full_name, city=contractor.city,
                                                                                 number=contractor.number_phone, balance=contractor.balance)
        await message.answer(text, reply_markup=await main_menu_contractors(reg))
