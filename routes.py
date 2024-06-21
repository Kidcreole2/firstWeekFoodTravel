import pprint
import json

from flask import (
    request,
    render_template,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
    jsonify,
)
from flask_login import logout_user, current_user, login_required
from core import app, login_manager
from models import *

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


# --status update--
@app.route("/goods/<int:goods_id>", methods=["GET", "POST"])
@login_required
def goods_data(goods_id):
    goods = Goods.query.filter_by(id=goods_id).first()
    if request.method == "POST":
        return jsonify({"name": goods.title, "price": goods.price}), 200
    return render_template("good_page.html", goods=goods)


@app.route("/ingridient/<int:ingridient_id>", methods=["POST"])
@login_required
def ingridient(ingridient_id):
    ingridient = Ingridient.query.filter_by(id=ingridient_id).first()
    return jsonify({"title": ingridient.title}), 200


@app.route("/order/update/<int:order_id>", methods=["POST"])
@login_required
def orders_update_status(order_id):
    old_order = Order.query.filter_by(id=order_id).first()
    if request.method == "POST":
        new_order = Order(
            delivery_to_address=old_order.delivery_to_address,
            delivery_from_address=old_order.delivery_from_address,
            delivery_date=old_order.delivery_date,
            status=request.form["status"],
            comment=old_order.comment,
            price=old_order.price,
        )
        Order.update(old_order, new_order)
        return jsonify({"message": "Заказ был успешно обновлён"}), 200
    
    
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
            role="client",
            phone_number=request.form["phone"],
        )
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
