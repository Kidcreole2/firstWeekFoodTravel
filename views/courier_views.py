from core import app
from flask import request, render_template
from flask_login import login_required,current_user
from models import *

def init_courier_views():
    @app.route("/index/courier", methods=["GET"])
    @login_required
    def courier_index():
        orders = User_Order.query.filter(
            User_Order.order.has(Order.status == "wait courier")
        ).all()
        active_orders = User_Order.query.filter(
            User_Order.user_id == current_user.id,
            User_Order.order.has(Order.status == "on the way"),
        ).all()
        return render_template(
            "courier/index.html", orders=orders, activer_orders=active_orders
        )
            
    @app.route("/order/update/courier/<int:order_id>")
    @login_required
    def orders_get_courier_id(order_id):
        if request.method == "POST":
            new_user_order = User_Order(user_id=current_user.id, order_id=order_id)
            User_Order.create(new_user_order)
