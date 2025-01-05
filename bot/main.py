import multiprocessing
import json
from contextlib import asynccontextmanager

from aiogram.types import FSInputFile
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.media_group import MediaGroupBuilder
from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from database import get_async_session, engine, Base
from fixtures import create_services
from keyboards import offer_order, menu_button
from repositories import ContractRepository, OrderRepository
from utils import user_text

TOKEN_BOT = "7608889792:AAFBc2jXoxRuOhnDOtjZLNnWvKYt8RJh1HU"

bot = Bot(TOKEN_BOT)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await create_services()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan, title="Contactors Bot")
app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
)


@app.post('/payment')
async def payment_notification(request: Request):
    if request.method == 'POST':
        body = await request.form()
        try:
            label = body.get('label')  # Получаем 'description' из данных формы
            user_id, price = label.split(':')
            await ContractRepository.up_balance(int(user_id), int(price))
            user, orders = await asyncio.gather(ContractRepository.get_contractor_with_services(int(user_id)),
                                                OrderRepository.get_active_orders())
            await bot.send_message(int(user_id),
                                   text=f"Оплата прошла успешно\n\n"
                                        f"Ваш баланс пополнен на {price} рублей.",
                                   reply_markup=menu_button)
            if orders:
                for order in orders:
                    if order.service in user.services:
                        text = order.description + "\n\n" + f"Услуга - {order.service.name}"
                        media_group = MediaGroupBuilder(caption=text)
                        if order.photo_path:
                            files_list = order.photo_path.split('\n')
                            for path_file in files_list[:len(files_list) - 1]:
                                if path_file:
                                    if files_list[0].split('.')[1].lower() in ['jpeg', 'png', 'jpg', 'svg', 'gif', 'raw',
                                                                               'tiff']:
                                        media = FSInputFile(path_file)
                                        media_group.add_photo(media=media)
                                    else:
                                        media = FSInputFile(path_file)
                                        media_group.add_document(media=media)
                            keyboard = await offer_order(user.id_telegram, order.id)
                            if order.photo_path:
                                await bot.send_media_group(user.id_telegram, media=media_group.build())
                                await bot.send_message(chat_id=user.id_telegram,
                                                       text=user_text.text_order,
                                                       reply_markup=keyboard,
                                                       parse_mode='Markdown')
                            else:
                                await bot.send_message(chat_id=user.id_telegram,
                                                       text=text)
                                await bot.send_message(chat_id=user.id_telegram,
                                                       text=user_text.text_order,
                                                       reply_markup=keyboard,
                                                       parse_mode='Markdown')
        except Exception as ex:
            return JSONResponse(content={"status": "success"}, status_code=200)
    return JSONResponse(content={"status": "success"}, status_code=200)


def start_fastapi():
    config = uvicorn.Config(app, host='0.0.0.0', port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()


async def main():
    from handlers import rout_comm, rout_callback, rout_messages
    fastapi_process = multiprocessing.Process(target=start_fastapi)
    fastapi_process.start()
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(rout_comm)
    dp.include_router(rout_callback)
    dp.include_router(rout_messages)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
