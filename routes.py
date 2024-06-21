import pprint

from flask import (
    request,
    render_template,
    redirect,
    flash,
    get_flashed_messages,
    jsonify,
)
from flask_simple_captcha import CAPTCHA
from flask_login import logout_user, current_user, login_required
from core import app, login_manager, SIMPLE_CAPTCHA
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

@app.route('/captcha/get', methods=['GET'])
def captcha_get():
    if request.method == 'GET':
        new_captcha_dict = SIMPLE_CAPTCHA.create()
        return new_captcha_dict

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        new_captcha_dict = SIMPLE_CAPTCHA.create()
        return new_captcha_dict
    if request.method == "POST":
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')
        if SIMPLE_CAPTCHA.verify(c_text, c_hash):
            login = request.form["login"]
            print(login)
            password = request.form.get("password")
            roles = User.auth_user(login, password)
            flash("wrong password/login")
            pprint.pprint(roles)
            return redirect("/")
        else:
            flash("wrong captcha")  
    messages = get_flashed_messages()
    return render_template("login.html", messages=messages)


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
