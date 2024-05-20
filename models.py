from flask_login import UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from core import app
import datetime, string, random
db = SQLAlchemy(app)

class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    role = db.Column(db.String(20),nullable=False)
    phone_number = db.Column(db.String(20))

    # связи
    users_orders = db.relationship("Users_Orders", back_populates="users", cascade="all, delete")
    
    
    def __init__(self, login: str,phone_number: str, password: str, firstname: str, lastname: str, surname: str, role: str):
        self.login = login
        self.password = password
        self.lastname = lastname
        self.firstname = firstname
        self.surname = surname
        self.role = role
        self.phone_number = phone_number
    
    @staticmethod
    def auth_user(login, password) -> dict:
        user = Users.query.filter_by(login=login).first()
        print(user)
        if user is not None and user.password == password:
            login_user(user)
            return {"role": user.role, "message": "", "id": user.id}
        else:
            return {"message": "Пользователь с таким логином уже существует придумайте другой", "role": ""}
    
    @staticmethod
    def create(user) -> dict:
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
        old_user.phone_number = new_user.phone_number
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
              
class Goods(db.Model):
    __tablename__ = "goods"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20),unique=True,nullable=False)
    photo_URL = db.Column(db.String(250))
    description = db.Column(db.String(300))
    price = db.Column(db.Integer, nullable=False)
    
    # связи
    goods_orders = db.relationship("Goods_Orders", back_populates="goods", cascade="all, delete")
    ingridients = db.relationship("Ingridient", back_populates="goods", cascade="all, delete")
    def __init__(self, title: str, price: int, photo_URL = "", description = ""):
        self.title = title
        self.photo_URL = photo_URL
        self.description = description
        self.price = price
        
    @staticmethod
    def create(goods):
        new_goods = Goods.query.filter_by(id=goods.id).first()
        if new_goods is None:
            db.session.add(goods)
            db.session.commit()
            return Goods.query.filter_by(id=goods.id).first().id
        else: 
            return new_goods.id
        
    @staticmethod
    def update(old_goods, new_goods):
        old_goods = Goods.query.filter_by(id=new_goods.id).first()
        old_goods.title = new_goods.title
        old_goods.photo_URL = new_goods.photo_URL
        old_goods.description = new_goods.description
        old_goods.price = new_goods.price
        db.session.commit()

    @staticmethod
    def delete(goods_id):
        Goods.query.filter_by(id=goods_id).delete()
        db.session.commit()
    
class Orders(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    delivery_address = db.Column(db.String(50),nullable=False)
    delivery_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.String(300))
    price = db.Column(db.Integer, nullable=False)
    
    # связи
    users_orders = db.relationship("Users_Orders", back_populates="orders", cascade="all, delete")
    goods_orders = db.relationship("Goods_Orders", back_populates="orders", cascade="all, delete")
    
    def __init__(self, delivery_address: str, delivery_date: datetime.datetime, status: str, comment: str, price: int):
        self.delivery_address = delivery_address
        self.delivery_date = delivery_date
        self.status = status
        self.comment = comment
        self.price = price
        
    @staticmethod
    def create(order):
        new_order = Orders.query.filter_by(id=order.id).first()
        if new_order is None:
            db.session.add(order)
            db.session.commit()
            return Orders.query.filter_by(id=order.id).first().id
        else: 
            return new_order.id
        
    @staticmethod
    def update(old_order, new_order):
        old_order = Orders.query.filter_by(id=old_order.id).first()
        old_order.delivery_address = new_order.delivery_address
        old_order.delivery_date = new_order.delivery_date
        old_order.status = new_order.status
        old_order.comment = new_order.comment
        old_order.price = new_order.price
        db.session.commit()

    @staticmethod
    def delete(order_id):
        Orders.query.filter_by(id=order_id).delete()
        db.session.commit()
            
class Ingridient(db.Model):
    __tablename__ = "ingridient"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20),nullable=False)
    goods_id = db.Column(db.Integer, db.ForeignKey("goods.id"))
    
    # связи
    ingridient_orders = db.relationship("Ingridient_Orders", back_populates="ingridient", cascade="all, delete")
    goods = db.relationship("Goods", back_populates="ingridient")
    
    def __init__(self, title: str, goods_id: int):
        self.title = title
        self.goods_id = goods_id
        
    @staticmethod
    def create(ingridient):
        new_ingridient = Ingridient.query.filter_by(id=ingridient.id).first()
        if new_ingridient is None:
            db.session.add(ingridient)
            db.session.commit()
            return Ingridient.query.filter_by(id=ingridient.id).first().id
        else: 
            return new_ingridient.id
        
    @staticmethod
    def update(old_ingridient, new_ingridient):
        old_ingridient = Ingridient.query.filter_by(id=old_ingridient.id).first()
        old_ingridient.title = new_ingridient.title
        old_ingridient.goods_id = new_ingridient.goods_id
        db.session.commit()

    @staticmethod
    def delete(ingridient_id):
        Ingridient.query.filter_by(id=ingridient_id).delete()
        db.session.commit()
    
class Users_Orders(db.Model):
    __tablename__ = "users_orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))

    # связи
    users = db.relationship("Users", back_populates="users_orders")
    order = db.relationship("Order", back_populates="users_orders")
    
    def __init__(self, user_id: int, order_id: int):
        self.user_id = user_id
        self.order_id = order_id
        
    @staticmethod
    def create(users_orders):
            db.session.add(users_orders)
            db.session.commit()
            
    @staticmethod
    def delete_by_user(user_id):
        users = Users_Orders.query.filter_by(user_id=user_id).all()
        for user in users:
            Users_Orders.query.filter_by(user_id=user.id).delete()
        db.session.commit()
    
    @staticmethod
    def delete_by_order(order_id):
        orders = Users_Orders.query.filter_by(order_id=order_id).all()
        for order in orders:
            Users_Orders.query.filter_by(order_id=order.id).delete()
        db.session.commit()
    
class Goods_Orders(db.Model):
    __tablename__ = "goods_orders"
    id = db.Column(db.Integer, primary_key=True)
    goods_id = db.Column(db.Integer, db.ForeignKey("goods.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))

    # связи
    goods = db.relationship("Goods", back_populates="goods_orders")
    order = db.relationship("Order", back_populates="goods_orders")
    ingridient_orders = db.relationship("Ingridient_Orders", back_populates="goods_orders", cascade="all, delete")
    
    def __init__(self, goods_id: int, order_id: int):
        self.goods_id = goods_id
        self.order_id = order_id
        
    @staticmethod
    def create(goods_orders):
            db.session.add(goods_orders)
            db.session.commit()
            
    @staticmethod
    def delete_by_goods(goods_id):
        goodses = Goods_Orders.query.filter_by(goods_id=goods_id).all()
        for goods in goodses:
            Goods_Orders.query.filter_by(goods_id=goods.id).delete()
        db.session.commit()
    
    @staticmethod
    def delete_by_order(order_id):
        orders = Goods_Orders.query.filter_by(order_id=order_id).all()
        for order in orders:
            Goods_Orders.query.filter_by(order_id=order.id).delete()
        db.session.commit()

class Ingridient_Orders(db.Model):
    __tablename__ = "ingridient_orders"
    id = db.Column(db.Integer, primary_key=True)
    ingridient_id = db.Column(db.Integer, db.ForeignKey("goods.id"))
    goods_orders_id = db.Column(db.Integer, db.ForeignKey("goods_orders.id"))

    # связи
    goods_orders = db.relationship("Goods_Orders", back_populates="ingridient_orders")
    ingridient = db.relationship("Ingridient", back_populates="ingridient_orders")
    
    def __init__(self, goods_id: int, order_id: int):
        self.goods_id = goods_id
        self.order_id = order_id
        
    @staticmethod
    def create(goods_orders):
            db.session.add(goods_orders)
            db.session.commit()
        

with app.app_context():
    db.create_all()