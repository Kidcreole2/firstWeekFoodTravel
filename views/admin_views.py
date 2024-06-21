from core import app
from flask import render_template, request, redirect
from flask_login import login_required
from models import User


def init_admin_views():
    @app.route("/index/admin", methods=["GET"])
    @login_required
    def admin_index():
        managers = User.query.filter(User.role == "manager").all()
        couriers = User.query.filter(User.role == "courier").all()
        kitchen = User.query.filter(User.role == "kitchen").all()
        return render_template(
            "admin/index.html", managers=managers, couriers=couriers, kitchens=kitchen
        )

    @app.route("/admin/user/create/<string:role>", methods=["GET", "POST"])
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
                        phone_number=request.form["phone"],
                    )
                    User.create(user)
                    return redirect("/index/admin")

                return render_template("admin/stuff-form.html", role=role)
            case "kitchen":
                if request.method == "POST":
                    user = User(
                        lastname="1",
                        firstname=request.form["address"],
                        surname="3",
                        login=request.form["login"],
                        password=request.form["password"],
                        role="kitchen",
                        phone_number="1",
                    )
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
                        phone_number=request.form["phone"],
                    )
                    User.create(user)
                    return redirect("/index/admin")
                return render_template("admin/stuff-form.html", role=role)

    @app.route("/admin/user/update/<int:user_id>", methods=["GET", "POST"])
    @login_required
    def user_update(user_id):
        old_user = User.query.filter_by(id=user_id).first()
        if request.method == "POST":
            if old_user.role == "kitchen":
                new_user = User(
                    lastname=old_user.lastname,
                    firstname=request.form["address"],
                    surname=old_user.surname,
                    login=request.form["login"],
                    password=request.form["password"],
                    role=old_user.role,
                    phone_number=old_user.phone_number,
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
                    phone_number=request.form["phone"],
                )

                User.update(old_user_id=user_id, new_user=new_user)
            return redirect("/index/admin")
        if old_user.role == "kitchen":
            return render_template("admin/kitchen-form.html", kitchen=old_user)
        else:
            return render_template("admin/stuff-form.html", old_user=old_user)
