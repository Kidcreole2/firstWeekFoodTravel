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
            # GoodsList
            return render_template("pages/client.html")
        case "kitchen":
            # OrderList(in kitchen)
            return render_template("pages/kitchen.html")
        case "courier":
            # OrderList(on the way)
            return render_template("pages/courier.html")
        case "manager":
            # OrderList(in processing)
            # GoodsList
            return render_template("pages/manager.html")
        
# ==Orders crud==

@app.route("/orders/<action>/<order_id>")
@login_required
def orders_actions(action,order_id):
    match action:
        case "create":
        case "update":
        case "delete":
        case "get":

# ==Goods crud==    
 
@app.route("/goods/<action>/<order_id>")
@login_required
def goods_actions(action,order_id):
    match action:
        case "create":
        case "update":
        case "delete":
            
# ==utilite functions folder==

@app.route("/upload_specs", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            save_file(file, "specs")
            flash("Файл успешно загружен")
            return redirect(request.url)
        else:
            flash("неверный тип файла")
    messages = get_flashed_messages()
    print(messages)
    return render_template("test/file_upload.html", messages=messages)


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
