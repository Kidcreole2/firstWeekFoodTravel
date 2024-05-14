from flask import request, render_template, redirect, url_for, flash, get_flashed_messages, jsonify
from flask_login import logout_user, current_user, login_required
from core import app, login_manager
from models import *
from file_manager import allowed_file, save_file


@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


# ==Home Pages==

@app.route("/index/<role>")
@login_required
def index(role):
    match role:
        case "client":
            goodses = Goods.query.all()
            return render_template("pages/client.html", goodses=goodses)
        case "kitchen":
            orders = Orders.query.filter_by(status="on kitchen").all()
            return render_template("pages/kitchen.html", orders=orders)
        case "courier":
            orders = Orders.query.filter_by(status="on the way").all()
            return render_template("pages/courier.html", orders=orders)
        case "manager":
            goodses = Goods.query.all()
            return render_template("pages/manager.html", goodses=goodses)
        
# ==crud==
        
# --Create entity--

@app.route("/<entity>/create")
@login_required
def create_entity(entity):
    match entity:
        case "order":
            if request.method == "POST":
                new_order = Orders(
                    delivery_address=request.form['delivery_address'],
                    delivery_date=request.form['delivery_date'],
                    status=request.form['status'],
                    comment=request.form['comment'],
                    price=request.form['price']
                )
                Orders.create(new_order)
                return jsonify({"message": "Заказ был успешно создан"}), 200
            return render_template("pages")
        case "goods":
            if request.method == "POST":
                new_goods = Goods(
                    delivery_address=request.form['delivery_address'],
                    delivery_date=request.form['delivery_date'],
                    status=request.form['status'],
                    comment=request.form['comment'],
                    price=request.form['price']
                )
                Goods.create(new_goods)
                return jsonify({"message": "Блюдо было успешно создано"}), 200
            return render_template("pages")
        case "ingridient":
            if request.method == "POST":
                new_ings = Ingridient(
                    title=request.form['title'],
                    goods_id=request.form['goods_id']
                )
                Ingridient.create(new_ings)
                return jsonify({"message": "Ингридиент был успешно создан"}), 200
            return render_template("pages")
        
# --status update--

@app.route("/order/update/<order_id>/<order_status>")
@login_required
def orders_update_status(order_id):
        old_order = Orders.query.filter_by(id=order_id).first()
        if request.method == "POST":
            new_order = Orders(
                delivery_address=old_order.delivery_address,
                delivery_date=old_order.delivery_date,
                status=request.form['status'],
                comment=old_order.comment,
                price=old_order.price
            )
            Orders.update(old_order,new_order)
            return jsonify({"message": "Заказ был успешно обновлён"}), 200
        return render_template("pages/opop/group/update.html")

# ==entity update/delete==    
 
@app.route("/<entity>/<action>/<entity_id>")
@login_required
def entity_actions(entity,action,entity_id):
    match entity:
        case "ingridient":
            match action:
                case "update":
                    old_goods = Goods.query.filter_by(id=entity_id).first()
                    if request.method == "POST":
                        new_goods = Goods(
                            delivery_address=request.form['delivery_address'],
                            delivery_date=request.form['delivery_date'],
                            status=request.form['status'],
                            comment=request.form['comment'],
                            price=request.form['price']
                        )
                        Goods.update(old_goods,new_goods)
                        return jsonify({"message": "Блюдо было успешно обновлено"}), 200
                    return render_template("pages/opop/group/update.html")
                case "delete":
                    return "Delete"
        case "goods":
            match action:
                case "update":
                    old_ings = Ingridient.query.filter_by(id=entity_id).first()
                    if request.method == "POST":
                        new_ings = Ingridient(
                            title=request.form['title'],
                            goods_id=request.form['goods_id']
                        )
                        Ingridient.update(old_ings,new_ings)
                        return jsonify({"message": "Ингридиент был успешно обновлён"}), 200
                    return render_template("pages/opop/group/update.html")
                case "delete":
                    return "Delete"
                
#  ==Users crud==

@app.route("/admin/user/create/<role>", methods=["GET", "POST"])
@login_required
def user_create(role):
    match role:
        case "client":
            if request.method == "POST":
                name = request.form["fio"].split(" ")
                user = Users(lastname=name[0], firstname=name[1], surname=name[2] if len(name) == 3 else " ", \
                    login=request.form["login"], password=request.form["password"],\
                        role="client",
                        phone_number=request.form["phone_number"])
                Users.create(user)           
                return jsonify({"message": "Пользователь был успешно создан"})

            return render_template("pages")
        case "courier":
            if request.method == "POST":
                name = request.form["fio"].split(" ")
                user = Users(lastname=name[0], firstname=name[1], surname=name[2] if len(name) == 3 else " ", \
                    login=request.form["login"], password=request.form["password"],\
                        role="courier",
                        phone_number=request.form["phone_number"]
                        )
                Users.create(user)           
                return jsonify({"message": "Пользователь был успешно создан"})

            return render_template("pages")
        case "kitchen":
            if request.method == "POST":
                user = Users(lastname="", firstname="", surname="", \
                    login=request.form["login"], password=request.form["password"],\
                    role="kitchen")
                Users.create(user)           
                return jsonify({"message": "Пользователь был успешно создан"})

            return render_template("pages")
        case "manager":
            if request.method == "POST":
                name = request.form["fio"].split(" ")
                user = Users(lastname=name[0], firstname=name[1], surname=name[2] if len(name) == 3 else " ", \
                    login=request.form["login"], password=request.form["password"],\
                        role="manager",
                        phone_number=request.form["phone_number"]
                        )
                Users.create(user)           
                return jsonify({"message": "Пользователь был успешно создан"})

            return render_template("pages")
    
@app.route("/admin/user/update/<user_id>", methods=["GET", "POST"])
@login_required
def user_update(user_id):
    old_user = Users.query.filter_by(id=user_id).first()                       
    if request.method == "POST":
        name = request.form["fio"].split()
        role = request.form["role"]
        
        new_user = Users(
            login=request.form["login"],
            password=request.form["password"],
            lastname=name[0],
            firstname=name[1],
            surname= name[2] if len(name) == 3 else " ",
            role=role,
            phone_number=""
            )
        
        Users.update(old_user_id=user_id, new_user=new_user)
        return jsonify({ "message": "Данные успешно обновлены" })
    
    return render_template("pages/admin/user/update.html", old_user=old_user)
# ==Basic functions==


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/home")
@login_required
def home():
    role = current_user.role
    match role:
        case "client":
            return render_template("pages/client.html")
        case "kitchen":
            return render_template("pages/kitchen.html")
        case "courier":
            return render_template("pages/courier.html")
        case "manager":
            return render_template("pages/manager.html")


# --login function--

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO make password check
        login = request.form["login"]
        print(login)
        password = request.form.get("password")
        roles = Users.auth_user(login, password)["role"]
        roles = roles.split
        return render_template("index.html", roles=roles)
    return render_template("login.html")

# --create user function--
