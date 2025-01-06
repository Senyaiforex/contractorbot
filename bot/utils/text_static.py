from dataclasses import dataclass
import os

@dataclass(frozen=True)
class AdminInterfaceData:
    """
    Статический текст для админов
    """
    text_start = ("Чтобы добавить объявление нажмите «Разместить заказ»\n"
                  "Чтобы отредактировать список услуг нажмите «Список услуг»\n"
                  "Для того, чтобы заблокировать(разблокировать подрядчика) "
                  "нажмите «Заблокировать подрядчика» или «Разблокировать подрядчика»")
    super_admin_text = ("Для просмотра статистики нажмите «Статистика»\n"
                        "Для того, чтобы заблокировать(разблокировать подрядчика) "
                        "нажмите «Заблокировать подрядчика» или «Разблокировать подрядчика»")
    name_order = "Введите текст для заявки"
    photo_order = ("Отправьте фотографии(файлы) заявки по одному сообщению.\n"
                   "После нажмите кнопку 'Готово'")
    services_order = "Выберите нужную услугу для заявки"
    client_name = "Введите имя клиента"
    client_phone = "Введите номер телефона клиента в формате +7 XXX XXX XX XX"




@dataclass(frozen=True)
class UserInterfaceData:
    """
    Статический текст для подрядчиков
    """
    text_constr = ("ФИО - {fio}\n"
                   "Город - {city}\n"
                   "Номер телефона - {number}\n"
                   "Баланс - {balance} ₽.\n"
                   "Дата регистрации - {date_reg}")
    text_start = ("👋 Добро пожаловать в бот «Бери Лиды»!\n\n"
                  "Здесь вы найдете свежие заявки от клиентов по вашей нише.\n"
                  "✅ Регистрируйтесь, выбирайте категорию и подписку.\n"
                  "✅ Получайте заказы и увеличивайте доход.\n\n"
                  "Нажмите “Регистрация”, чтобы приступить!")
    reg_text = "Регистрация"
    fio_question = ("Введите Ваши ФИО через пробел\n"
                    "Пример: Иванов Иван Иванович")
    phone_question = ("Введите ваш номер телефона в формате +7 XXX XXX XX XX\n"
                    "Пример: +7 123 456 78 90")
    city_question = ("Введите Ваш город\n"
                     "Пример: Москва")
    company_question = "Введите название Вашей компании"
    site_question = "Отправьте ссылку на сайт или нажмите кнопку «Пропустить»"
    activity_question = "Выберите основной вид деятельности"
    social_question = "Введите ссылки на ваши соц сети через пробел"
    reg_finish = ("🎉 Поздравляем, вы успешно зарегистрировались!\n\n"
                  "Теперь вы будете получать актуальные заявки по выбранной нише.\n"
                  "📩 Как только появится подходящий заказ, мы сразу вам сообщим!\n\n"
                  "Удачных сделок и отличного заработка! 🚀")
    text_order = ("Берете заказ в работу?\n\n"
                  "_\rС баланса спишется сумма за заказ в размере 100₽_\r")
    text_order_try = ("Берете заказ в работу?\n\n"
                      "После того, как вы возьмете заказ в работу, "
                      "вам будут доступны контактные данные клиента.")
user_text = UserInterfaceData()
admin_text = AdminInterfaceData()
