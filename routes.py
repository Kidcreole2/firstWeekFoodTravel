from flask import request, render_template, redirect, url_for, flash, get_flashed_messages, jsonify
from flask_login import logout_user, current_user, login_required
from core import app, login_manager
from models import *


@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


# ==Home Pages==

@app.route("/index/<role>")
@login_required
def index(role):
    match role:
        case "kitchen":
            orders_on_kitchen = Order.query.filter_by(status="on kitchen").all()
            orders_wait_kitchen = Order.query.filter_by(status="waiting kitchen").all()
            orders_wait_courier = Order.query.filter_by(status="waiting courier").all()
            return render_template("kitchen/index.html", orders_wait_kitchen=orders_wait_kitchen,
                                   orders_on_kitchen=orders_on_kitchen, orders_wait_courier=orders_wait_courier)
        case "courier":
            orders = User_Order.query.filter(User_Order.status == "waiting courier").all()
            active_orders = User_Order.query.filter(User_Order.has(User_Order.user_id == current_user.id),
                                                      User_Order.users.has(User.status == "on the way")).all()
            return render_template("courier/index.html", orders=orders, activer_orders=active_orders)
        case "manager":
            goodses = Goods.query.all()
            return render_template("manager/index.html", goodses=goodses)
        case "admin":
            managers = User.query.filter(User.role == "manager").all()
            couriers = User.query.filter(User.role == "courier").all()
            kitchen = User.query.filter(User.role == "kitchen").all()
            return render_template("admin/index.html", managers=managers, couriers=couriers, kitchen=kitchen)


# ==crud==

# --Create entity--

@app.route("/<entity>/create")
@login_required
def create_entity(entity):
    match entity:
        case "order":
            if request.method == "POST":
                new_order = Order(delivery_address=request.form['delivery_address'],
                    delivery_date=request.form['delivery_date'], status=request.form['status'],
                    comment=request.form['comment'], price=request.form['price'])
                new_order_id = Order.create(new_order)
                goodses = []
                for goods in goodses:
                    new_goods_order = Goods_Order(goods_id=goods, order_id=new_order_id)
                return jsonify({"message": "Заказ был успешно создан"}), 200
            return render_template("pages/orders/cart.html")
        case "goods":
            if request.method == "POST":
                new_goods = Goods(title=request.form['title'], photo_URL=request.form['photo_URL'],
                    description=request.form['description'], price=request.form['price'], )
                Goods.create(new_goods)
                return jsonify({"message": "Блюдо было успешно создано"}), 200
            return render_template("pages/goods/create.html")
        case "ingridient":
            if request.method == "POST":
                new_ings = Ingridient(title=request.form['title'], goods_id=request.form['goods_id'])
                Ingridient.create(new_ings)
                return jsonify({"message": "Ингридиент был успешно создан"}), 200
            return render_template("pages/goods/ingridients/create.html")


# --status update--

@app.route("/order/update/<order_id>")
@login_required
def orders_update_status(order_id):
    old_order = Order.query.filter_by(id=order_id).first()
    if request.method == "POST":
        new_order = Order(delivery_address=old_order.delivery_address, delivery_date=old_order.delivery_date,
            status=request.form['status'], comment=old_order.comment, price=old_order.price)
        Order.update(old_order, new_order)
        return jsonify({"message": "Заказ был успешно обновлён"}), 200


# ==entity update/delete==

@app.route("/<entity>/<action>/<entity_id>")
@login_required
def entity_actions(entity, action, entity_id):
    match entity:
        case "goods":
            match action:
                case "update":
                    old_goods = Goods.query.filter_by(id=entity_id).first()
                    if request.method == "POST":
                        new_goods = Goods(title=request.form['title'], photo_URL=request.form['photo_URL'],
                            description=request.form['description'], price=request.form['price'], )
                        Goods.update(old_goods, new_goods)
                        return jsonify({"message": "Блюдо было успешно обновлено"}), 200
                    return render_template("pages/goods/update.html")
                case "delete":
                    return "Delete"
        case "ingridient":
            match action:
                case "update":
                    old_ings = Ingridient.query.filter_by(id=entity_id).first()
                    if request.method == "POST":
                        new_ings = Ingridient(title=request.form['title'], goods_id=request.form['goods_id'])
                        Ingridient.update(old_ings, new_ings)
                        return jsonify({"message": "Ингридиент был успешно обновлён"}), 200
                    return render_template("pages/ingridients/update.html")
                case "delete":
                    return "Delete"


#  ==Users crud==

@app.route("/admin/user/create/<role>", methods=["GET", "POST"])
@login_required
def user_create(role):
    match role:
        case "courier":
            if request.method == "POST":
                name = request.form["fio"].split(" ")
                user = User(
                    lastname=request.form["lastname"],
                    firstname=request.form["firstname"],
                    surname=request.form["surname"],
                    login=request.form["login"],
                    password=request.form["password"],
                    role="client",
                    phone_number=request.form["phone_number"]
                    )
                User.create(user)
                return jsonify({"message": "Пользователь был успешно создан"})

            return render_template("pages")
        case "kitchen":
            if request.method == "POST":
                user = User(lastname="", firstname="", surname="", login=request.form["login"],
                             password=request.form["password"], role="kitchen")
                User.create(user)
                return jsonify({"message": "Пользователь был успешно создан"})

            return render_template("pages")
        case "manager":
            if request.method == "POST":
                name = request.form["fio"].split(" ")
                user = User(
                    lastname=request.form["lastname"],
                    firstname=request.form["firstname"],
                    surname=request.form["surname"],
                    login=request.form["login"],
                    password=request.form["password"],
                    role="client",
                    phone_number=request.form["phone_number"]
                    )
                User.create(user)
                return jsonify({"message": "Пользователь был успешно создан"})

            return render_template("pages")


@app.route("/admin/user/update/<user_id>", methods=["GET", "POST"])
@login_required
def user_update(user_id):
    old_user = User.query.filter_by(id=user_id).first()
    if request.method == "POST":
        name = request.form["fio"].split()
        role = request.form["role"]

        new_user = User(
            lastname=request.form["lastname"],
            firstname=request.form["firstname"],
            surname=request.form["surname"],
            login=request.form["login"],
            password=request.form["password"],
            role="client",
            phone_number=request.form["phone_number"]
            )

        User.update(old_user_id=user_id, new_user=new_user)
        return jsonify({"message": "Данные успешно обновлены"})

    return render_template("admin/stuff-form.html", old_user=old_user)


# ==Basic functions==


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("/login"))


# --login function--

app.route("/registration", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        user = User(
            lastname=request.form["lastname"],
            firstname=request.form["firstname"],
            surname=request.form["surname"],
            login=request.form["login"],
            password=request.form["password"],
            role="client",
            phone_number=request.form["phone_number"])
        User.create(user)
        return jsonify({"message": "Пользователь был успешно создан"})

    return render_template("pages")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO make password check
        login = request.form["login"]
        print(login)
        password = request.form.get("password")
        roles = User.auth_user(login, password)["role"]
        roles = roles.split
        return redirect("/")
    return render_template("login.html")

@app.route("/", methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        role = current_user.role
        match role:
            case "kitchen":
                return redirect("/index/kitchen")
            case "courier":
                return redirect("/index/courier")
            case "manager":
                return redirect("/index/manager")

        goods = Goods.query.order_by(Goods.title).all()
        return render_template("index.html", goods=goods)
    else:
        return redirect("/login")  # --create user function--
