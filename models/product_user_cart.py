from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey,  DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    photo = Column(String)
    name = Column(String)
    description = Column(String)
    price = Column(Float)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    cart_items = relationship('CartItem', backref="user")


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    product = relationship('Product', backref='card_items')

