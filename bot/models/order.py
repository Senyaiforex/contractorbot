from datetime import datetime

from sqlalchemy import Column, String, Integer, BigInteger, Boolean, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
import enum
from database import Base

class StatusEnum(enum.Enum):
    active = 'active'
    completed = 'completed'


class Order(Base):
    """
    Модель подрядчика
    """
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_telegram = Column(BigInteger, ForeignKey('contractors.id_telegram'))
    status = Column(Enum(StatusEnum), default=StatusEnum.active, comment="Статус заказа")
    description = Column(String(120), comment="Описание заказа")
    service_id = Column(Integer, ForeignKey('services.id'))
    photo_path = Column(String, comment="Путь к файлам")
    date = Column(Date, default=datetime.utcnow)
    client_name = Column(String(100), comment="Имя клиента для заказа")
    client_phone = Column(String(25), comment="Номер телефона клиента")
