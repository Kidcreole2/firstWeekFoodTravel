from core import app
from flask import request, render_template, jsonify
from flask_login import login_required, current_user
from sqlalchemy import and_
from models import *


def init_courier_views():
    @app.route("/index/courier", methods=["GET"])
    @login_required
    def courier_index():
        orders = []
        for order in Order.query.all():
            if order.status == "wait courier":
                if len(order.user_order) < 2:
                    orders.append(order)

        active_orders = User_Order.query.filter(
                User_Order.user_id == current_user.id,
        ).all()
        print(active_orders)
        for ao in active_orders:
            print(ao.order.status)
        active_orders = filter(lambda ao: (ao.order.status == 'in deliver'), active_orders)    
        print(active_orders)
        return render_template(
            "courier/index.html", orders=orders, activer_orders=active_orders
        )

    @app.route("/order/update/courier/<int:order_id>", methods=["POST"])
    @login_required
    def orders_get_courier_id(order_id):
        if request.method == "POST":
            new_user_order = User_Order(user_id=current_user.id, order_id=order_id)
            User_Order.create(new_user_order)
            return jsonify({"status": 200})
