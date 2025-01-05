from aiogram.fsm.state import StatesGroup, State



class RegStates(StatesGroup):
    """
    Состояния для работы при регистрации подрядчика
    """
    FULL_NAME = State()
    PHONE = State()
    CITY = State()
    COMPANY = State()
    SITE = State()
    SOCIAL = State()
    SERVICE = State()
    OTHER_SERVICE = State()

class ServiceState(StatesGroup):
    """
    Состояния для работы при регистрации услуги
    """
    NAME_SERVICE = State()

class OrderCreateState(StatesGroup):
    """
    Состояния для работы при создании заявки
    """
    text_order = State()
    photo_order = State()
    services_order = State()
    client_name_order = State()
    client_phone_order = State()
    edit_text_order = State()
