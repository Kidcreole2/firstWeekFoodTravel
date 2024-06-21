from core import app
from flask import render_template, request, redirect,jsonify
from flask_login import login_required,current_user
from models import *
from datetime import datetime as date


def init_manager_views():
    @app.route("/index/manager", methods=["GET"])
    @login_required
    def manager_index():
        orders_in_processing = Order.query.filter(
            Order.status == "in processing"
        ).all()
        orders_closed = Order.query.filter(
            Order.status == "delivered", Order.status == "deprecated"
        ).all()
        orders_others = Order.query.filter(
            Order.status != "in processing",
            Order.status != "deprecated",
            Order.status != "delivered",
        ).all()
        return render_template(
            "manager/index.html",
            orders_in_processing=orders_in_processing,
            orders_others=orders_others,
            orders_closed=orders_closed,
        )
            
    @app.route("/manager/goods", methods=["GET"])
    @login_required
    def manager_goods():
        goods = Goods.query.all()
        return render_template("manager/goods-page.html", goods=goods)
    
    @app.route("/<string:entity>/create", methods=["GET", "POST"])
    @login_required
    def create_entity(entity):
        match entity:
            case "order":
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
            case "goods":
                if request.method == "POST":
                    new_goods = Goods(
                        title=request.form["title"],
                        photo_URL=request.form["image-url"],
                        description=request.form["description"],
                        price=request.form["price"],
                    )
                    Goods.create(new_goods)
                    return redirect("/manager/goods")
                return render_template("manager/good-form.html")


    @app.route("/ingridient/<int:goods_id>/create", methods=["GET", "POST"])
    @login_required
    def create_ingridient(goods_id):
        if request.method == "POST":
            new_ings = Ingridient(title=request.form["title"], goods_id=goods_id)
            Ingridient.create(new_ings)
            return jsonify(
                {"goods_id": goods_id, "message": "Ингридиент был успешно создан"}
            )
        return render_template("manager/ingridients-form.html")
    
    @app.route("/goods/<string:action>/<int:goods_id>")
    @login_required
    def goods_actions(action, goods_id):
        match action:
            case "update":
                old_goods = Goods.query.filter_by(id=goods_id).first()
                if request.method == "POST":
                    new_goods = Goods(
                        title=request.form["title"],
                        photo_URL=request.form["image-url"],
                        description=request.form["description"],
                        price=request.form["price"],
                    )
                    Goods.update(old_goods, new_goods)
                    return redirect("/manager/goods")
                return render_template("manager/good-form.html", goods=old_goods)
            case "delete":
                Goods.delete(goods_id)
                return jsonify({"message": "Блюдо успешно удалено"}), 200


    @app.route("/ingridient/<string:action>/<int:ingridient_id>")
    @login_required
    def ingridiend_actions(action, ingridient_id):
        match action:
            case "update":
                old_ings = Ingridient.query.filter_by(id=ingridient_id).first()
                if request.method == "POST":
                    new_ings = Ingridient(
                        title=request.form["title"], goods_id=old_ings.goods_id
                    )
                    Ingridient.update(old_ings, new_ings)
                    return redirect(f"/goods/update/{old_ings.goods_id}")
                return render_template("manager/ingridients-form.html", ingridient=old_ings)
            case "delete":
                Ingridient.delete(ingridient_id)
                return jsonify({"message": "Ингредиент успешно удален"}), 200