from core import app
from flask import render_template
from flask_login import login_required
from models import *

def init_kitchen_views():
    @app.route("/index/kitchen", methods=["GET"])
    @login_required
    def kitchen_index():
        orders_on_kitchen = Order.query.filter_by(status="on kitchen").all()
        orders_wait_kitchen = Order.query.filter_by(status="waiting kitchen").all()
        orders_wait_courier = Order.query.filter_by(status="wait courier").all()
        return render_template(
            "kitchen/index.html",
            orders_wait_kitchen=orders_wait_kitchen,
            orders_on_kitchen=orders_on_kitchen,
            orders_wait_courier=orders_wait_courier,
        )

    @app.route("/order/list")
    @login_required
    def orders_list():
        orders_list = Order.query.all()
        return render_template("", orders_list=orders_list)
        
            
    # --order get--

    @app.route("/order/get/<int:order_id>")
    @login_required
    def orders_give_courier_id(order_id):
        order = Order.query.filter_by(id=order_id).first()
        return render_template("kitchen/order_page.html", order=order)