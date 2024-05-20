import pprint

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
            orders_in_processing = Order.query.filter(Order.status == "in processing").all()
            return render_template("manager/index.html", orders_in_processing=orders_in_processing)
        case "admin":
            managers = User.query.filter(User.role == "manager").all()
            couriers = User.query.filter(User.role == "courier").all()
            kitchen = User.query.filter(User.role == "kitchen").all()
            return render_template("admin/index.html", managers=managers, couriers=couriers, kitchens=kitchen)

@app.route('/manager/goods', methods=['GET'])
@login_required
def manager_goods():
    goods = Goods.query.all()
    return render_template('manager/goods-page.html', goods=goods)
# ==crud==

# --Create entity--

@app.route("/<entity>/create", methods=['GET', 'POST'])
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
                new_goods = Goods(title=request.form['title'], photo_URL=request.form['image-url'],
                    description=request.form['description'], price=request.form['price'], )
                Goods.create(new_goods)
                return redirect('/manager/goods')
            return render_template("manager/good-form.html")


@app.route('/ingridient/<goods_id>/create', methods=['GET', 'POST'])
@login_required
def create_ingridient(goods_id):
    if request.method == "POST":
        new_ings = Ingridient(title=request.form['title'], goods_id=goods_id)
        Ingridient.create(new_ings)
        return jsonify({"goods_id": goods_id, "message": "Ингридиент был успешно создан"})
    return render_template("manager/ingridients-form.html")

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

@app.route("/<entity>/<action>/<entity_id>", methods=['GET', 'POST'])
@login_required
def entity_actions(entity, action, entity_id):
    match entity:
        case "goods":
            match action:
                case "update":
                    old_goods = Goods.query.filter_by(id=entity_id).first()
                    if request.method == "POST":
                        new_goods = Goods(title=request.form['title'], photo_URL=request.form['image-url'],
                            description=request.form['description'], price=request.form['price'], )
                        Goods.update(old_goods, new_goods)
                        return redirect('/manager/goods')
                    return render_template("manager/good-form.html", goods=old_goods)
                case "delete":
                    Goods.delete(entity_id)
                    return jsonify({"message": "Блюдо успешно удалено"}), 200
        case "ingridient":
            match action:
                case "update":
                    old_ings = Ingridient.query.filter_by(id=entity_id).first()
                    if request.method == "POST":
                        new_ings = Ingridient(title=request.form['title'], goods_id=old_ings.goods_id)
                        Ingridient.update(old_ings, new_ings)
                        return redirect(f"/goods/update/{old_ings.goods_id}")
                    return render_template("manager/ingridients-form.html", ingridient=old_ings)
                case "delete":
                    Ingridient.delete(entity_id)
                    return jsonify({"message": "Ингредиент успешно удален"}), 200

@app.route("/user/cart_element/<goods_id>", methods=['POST'])
@login_required
def user_cart_element(goods_id):
    goods = Goods.query.filter_by(id=goods_id).first()
    return render_template("cart-element.html", goods=goods)


#  ==Users crud==

@app.route("/admin/user/create/<role>", methods=["GET", "POST"])
@login_required
def user_create(role):
    match role:
        case "courier":
            if request.method == "POST":
                user = User(
                    lastname=request.form["lastname"],
                    firstname=request.form["firstname"],
                    surname=request.form["surname"],
                    login=request.form["login"],
                    password=request.form["password"],
                    role="courier",
                    phone_number=request.form["phone"]
                    )
                User.create(user)
                return redirect("/index/admin")

            return render_template("admin/stuff-form.html", role=role)
        case "kitchen":
            if request.method == "POST":
                user = User(lastname="1", firstname="1", surname="1", login=request.form["login"],
                             password=request.form["password"], role="kitchen", phone_number="1")
                User.create(user)
                return redirect("/index/admin")

            return render_template("admin/kitchen-form.html", role=role)
        case "manager":
            if request.method == "POST":
                user = User(
                    lastname=request.form["lastname"],
                    firstname=request.form["firstname"],
                    surname=request.form["surname"],
                    login=request.form["login"],
                    password=request.form["password"],
                    role="manager",
                    phone_number=request.form["phone"]
                    )
                User.create(user)
                return redirect("/index/admin")
            return render_template("admin/stuff-form.html", role=role)


@app.route("/admin/user/update/<user_id>", methods=["GET", "POST"])
@login_required
def user_update(user_id):
    old_user = User.query.filter_by(id=user_id).first()
    if request.method == "POST":
        if old_user.role == "kitchen":
            new_user = User(
                lastname=old_user.lastname,
                firstname=old_user.firstname,
                surname=old_user.surname,
                login=request.form["login"],
                password=request.form["password"],
                role=old_user.role,
                phone_number=old_user.phone_number
            )

            User.update(old_user_id=user_id, new_user=new_user)
        else:
            new_user = User(
                lastname=request.form["lastname"],
                firstname=request.form["firstname"],
                surname=request.form["surname"],
                login=request.form["login"],
                password=request.form["password"],
                role=old_user.role,
                phone_number=request.form["phone"]
                )

            User.update(old_user_id=user_id, new_user=new_user)
        return redirect('/index/admin')
    if old_user.role == "kitchen":
        return render_template("admin/kitchen-form.html", kitchen=old_user)
    else:
        return render_template("admin/stuff-form.html", old_user=old_user)

# ==Basic functions==


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


# --login function--

@app.route("/registration", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        user = User(
            lastname=request.form["lastname"],
            firstname=request.form["firstname"],
            surname=request.form["surname"],
            login=request.form["login"],
            password=request.form["password"],
            role="admin",
            phone_number=request.form["phone"])
        pprint.pprint(User.create(user))
        return redirect("/")
    return render_template("registrate.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO make password check
        login = request.form["login"]
        print(login)
        password = request.form.get("password")
        roles = User.auth_user(login, password)
        pprint.pprint(roles)
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
            case "admin":
                return redirect("/index/admin")
        goods = Goods.query.order_by(Goods.title).all()
        return render_template("index.html", goods=goods)
    else:
        return redirect("/login")  # --create user function--
