from datetime import datetime

from sqlalchemy import Column, String, Integer, Table, ForeignKey, BigInteger, Boolean, Date
from sqlalchemy.orm import relationship
from database import Base
from .order import Order
services_contractors = Table(
        'services_contractors', Base.metadata,
        Column('id_telegram', ForeignKey('contractors.id_telegram', ondelete='CASCADE'),
               primary_key=True),
        Column('service_id', ForeignKey('services.id', ondelete='CASCADE'),
               primary_key=True),
)


class Contractors(Base):
    """
    Модель подрядчика
    """
    __tablename__ = 'contractors'
    id = Column(Integer, primary_key=True, index=True)
    id_telegram = Column(BigInteger, index=True, comment="Telegram ID", unique=True)
    user_name = Column(String, index=True, comment="Никнейм", unique=True)
    full_name = Column(String, comment="ФИО")
    number_phone = Column(String(length=25), comment="Номер телефона")
    city = Column(String(length=40), comment="Город")
    company = Column(String(length=120), comment="Название компании")
    social_media = Column(String(length=100), comment="Ссылки на социальные сети")
    site = Column(String(length=50), comment="Сайт")
    balance = Column(Integer, comment="Баланс внутри бота", default=0)
    services = relationship("Service",
                            secondary=services_contractors,
                            back_populates='contractors',
                            cascade="all, delete",
                            passive_deletes=True)
    orders = relationship("Order", backref='contractor')
    date_reg = Column(Date, default=datetime.utcnow, comment="Дата регистрации")
    free_try = Column(Boolean, comment="Бесплатная попытка", default=True)
    active = Column(Boolean, default=True, comment="Активный ли пользователь")
