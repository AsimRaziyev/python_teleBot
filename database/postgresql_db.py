import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload

from models.product_user_cart import Base, Product, User, CartItem
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")


def create_db_engine():
    db_url = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    return engine


def add_user(id, username, email, password, phone_number, address):
    engine = create_db_engine()
    session = sessionmaker(bind=engine)()
    user = User(id=id, username=username, email=email, password=password, phone_number=phone_number, address=address)
    session.add(user)
    session.commit()
    session.close()


def get_user_id(user_id):
    engine = create_db_engine()
    session = sessionmaker(bind=engine)()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()
    if user:
        return user.id
    return None


def get_all_products():
    engine = create_db_engine()
    session = sessionmaker(bind=engine)()
    products = session.query(Product).all()
    session.close()
    return products


def add_product(photo, name, description, price):
    engine = create_db_engine()
    session = sessionmaker(bind=engine)()
    product = Product(photo=photo, name=name, description=description, price=price)
    session.add(product)
    session.commit()
    session.close()


def delete_product(product_id):
    engine = create_db_engine()
    session = sessionmaker(bind=engine)()
    product = session.query(Product).filter_by(id=product_id).first()
    if product:
        session.delete(product)
        session.commit()
    session.close()


def add_product_to_cart_item(user_id, product_id, quantity):
    engine = create_db_engine()
    session = sessionmaker(bind=engine)()
    cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
    session.add(cart_item)
    session.commit()
    session.close()


def delete_product_from_cart(cart_id):
    engine = create_db_engine()
    session = sessionmaker(bind=engine)()
    cart_item_product = session.query(CartItem).filter_by(id=cart_id).first()
    if cart_item_product:
        session.delete(cart_item_product)
        session.commit()
    session.close()


def get_user_cart(user_id):
    engine = create_db_engine()
    session = sessionmaker(bind=engine)()
    cart_items = session.query(CartItem).options(joinedload(CartItem.product)).filter_by(user_id=user_id).all()
    session.close()
    return cart_items


