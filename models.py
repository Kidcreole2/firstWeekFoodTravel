from flask_login import UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from core import app
import datetime, string, random
#TODO создание админа
db = SQLAlchemy(app)

class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(20), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20),nullable=False)

    # связи
    users_orders = db.relationship("Users_Orders", back_populates="users")
    
    
    def __init__(self, login: str, password: str, firstname: str, lastname: str, surname: str, role):
        self.login = login
        self.password = password
        self.lastname = lastname
        self.firstname = firstname
        self.surname = surname
        self.role = role
    
    @staticmethod
    def auth_user(login, password) -> str:
        user = Users.query.filter_by(login=login).first()
        print(user)
        if user is not None and user.password == password:
            login_user(user)
            return {"role": user.role, "message": "", "id": user.id}
        else:
            return {"message": "Пользователь с таким логином уже существует придумайте другой", "role": ""}
    
    @staticmethod
    def create(user):
        new_user = Users.query.filter_by(login=user.login).first()
        if new_user is None:
            db.session.add(user)
            db.session.commit()
            return { "id":user.id, "exists": False, "role": user.role, "message": ""}
        else:
            return {"id": new_user.id, "exists": True, "message": "Пользователь с таким логином уже существует придумайте другой", "role": ""}
        
    @staticmethod 
    def update(old_user_id, new_user): 
        old_user = Users.query.filter_by(id=old_user_id).first()
        old_user.login = new_user.login
        old_user.password = new_user.password
        old_user.firstname = new_user.firstname
        old_user.lastname = new_user.lastname
        old_user.surname = new_user.surname
        db.session.commit()

    @staticmethod
    def delete(user_id):
        Users.query.filter_by(id=user_id).delete()
        db.session.commit()

    @staticmethod
    def password_generation():
        characters = string.ascii_letters + string.digits
        password = ""   
        for index in range(10):
            password = password + random.choice(characters)
        return password
    
    @staticmethod
    def login_generation():
        letters = string.ascii_uppercase
        digits = string.digits
        login = ""
        for index in range(10):
            if index > 3:
                login = login + random.choice(digits)
            else:
                login = login + random.choice(letters)
        return login

                
class Goods(UserMixin, db.Model):
    __tablename__ = "goods"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20),unique=True,nullable=False)
    photo_URL = db.Column(db.String(100))
    description = db.Column(db.String(300))
    price = db.Column(db.Integer, nullable=False)
    
    # связи
    goods_orders = db.relationship("Goods_Orders", back_populates="goods")
    
class Orders(UserMixin, db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    delivery_address = db.Column(db.String(50),nullable=False)
    delivery_date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.String(300))
    price = db.Column(db.Integer, nullable=False)
    
    # связи
    users_orders = db.relationship("Users_Orders", back_populates="orders")
    goods_orders = db.relationship("Goods_Orders", back_populates="orders")
    
class Ingridients(UserMixin, db.Model):
    __tablename__ = "ingridients"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20),unique=True,nullable=False)
    goods_id = db.Column(db.Integer, db.ForeignKey("goods.id"))
    
    # связи
    goods = db.relationship("Goods", back_populates="ingridients")
    
class Users_Orders(UserMixin, db.Model):
    __tablename__ = "users_orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))

    # связи
    users = db.relationship("Users", back_populates="users_orders")
    order = db.relationship("Order", back_populates="users_orders")
    
class Goods_Orders(UserMixin, db.Model):
    __tablename__ = "goods_orders"
    id = db.Column(db.Integer, primary_key=True)
    goods_id = db.Column(db.Integer, db.ForeignKey("goods.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))

    # связи
    goods = db.relationship("Goods", back_populates="goods_orders")
    order = db.relationship("Order", back_populates="goods_orders")
    
