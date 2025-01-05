from sqlalchemy import Column, String, Boolean, BigInteger, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from .users import services_contractors


class Service(Base):
    """
    Модель оказываемой услуги
    """
    __tablename__ = 'services'
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(length=100), index=True, comment="Название услуги")
    contractors = relationship("Contractors",
                               secondary=services_contractors,
                               back_populates='services',
                               cascade="all, delete",
                               passive_deletes=True)
    active = Column(Boolean, default=True)
    orders = relationship("Order",
                          backref='service')
