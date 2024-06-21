from core import app, SIMPLE_CAPTCHA
from flask import render_template, request, jsonify, redirect, flash, get_flashed_messages
from flask_login import login_required, current_user
from models import *
from datetime import datetime as date
import pprint
import json


def init_user_views():
    @app.route("/order/create", methods=["GET", "POST"])
    @login_required
    def create_order():
        if request.method == "POST":
            order_json = request.form["cart"]
            goodses = json.loads(order_json)
            print(goodses)
            for goods in goodses:
                print(goods["ingridients"])
            new_order = Order(
                delivery_from_address=request.form["addressFrom"],
                delivery_to_address=request.form["addressTo"],
                delivery_date=date.now(),
                status="in processing",
                comment=request.form["comment"],
                price=request.form["price"],
            )
            new_order_id = Order.create(new_order)
            new_user_order = User_Order(user_id=current_user.id, order_id=new_order_id)
            User_Order.create(new_user_order)
            for goods in goodses:
                new_goods_order = Goods_Order(
                    goods_id=goods["goods"], order_id=new_order_id
                )
                new_goods_order_id = Goods_Order.create(new_goods_order)
                ingridients = goods["ingridients"]
                for ingridient in ingridients:
                    new_ingridient_order = Ingridient_Order(
                        ingridient_id=ingridient, goods_order_id=new_goods_order_id
                    )
                    Ingridient_Order.create(new_ingridient_order)
            return jsonify({"message": "Заказ был успешно создан"}), 200
        kitchens = User.query.filter(User.role == "kitchen").all()
        return render_template("make-order.html", kitchens=kitchens)

    @app.route("/registration", methods=["GET", "POST"])
    def sign_up():
        if request.method == "POST":
            c_hash = request.form.get('captcha-hash')
            c_text = request.form.get('captcha-text')
            if SIMPLE_CAPTCHA.verify(c_text, c_hash):
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
            else: 
                return flash("неправильная каптча")
            
        messages = get_flashed_messages()
        new_captcha_dict = SIMPLE_CAPTCHA.create()
        return render_template("registrate.html", messages=messages, captcha=new_captcha_dict)
    
    @app.route('/orders', methods=['GET'])
    @login_required
    def user_orders():
        orders = current_user.user_order
        active_orders = []
        inactive_orders = []
        for order in orders:
            if order.order.status != 'deprecated' and order.order.status != 'delivered':
                active_orders.append(order.order)
            else: 
                inactive_orders.append(order.order)
        return render_template('orders-list.html', active_orders=active_orders, completed_orders=inactive_orders)