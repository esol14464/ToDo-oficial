from flask import Flask, render_template, redirect, url_for, flash, request
import config
from models import db, User
from flask_bootstrap import Bootstrap
from forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user, current_user, LoginManager

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        form = request.form
        user_email = form.get('email')
        user_password = form.get('password')
        user = User.query.filter_by(email=user_email).first()
        if not user:
            flash("Email not registered.", "error")
            return redirect(url_for("login"))
        if not user.is_correct_password(user_password):
            flash("Password incorrect.", "error")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        form = request.form
        user_email = form.get("email")
        user_password = form.get("password")
        user_name = form.get("name")
        if User.query.filter_by(email=user_email).first():
            flash("You've already signed up with that email.", "error")
            return redirect(url_for('register'))
        new_user = User(email=user_email, name=user_name, password=user_password)
        new_user.set_password(user_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(user=new_user)
        return redirect(url_for('home'))
    return render_template("register.html")


@app.route("/home")
@login_required
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
