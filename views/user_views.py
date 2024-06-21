from core import app
from flask import render_template, request, jsonify
from flask_login import login_required,current_user
from models import *
from datetime import datetime as date
import json

def init_user_views():
    @app.route("/order/create", methods=["GET", "POST"])
    @login_required
    def create_entity():
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
            new_user_order = User_Order(
                user_id=current_user.id, order_id=new_order_id
            )
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