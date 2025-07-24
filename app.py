from flask import Flask, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask_bcrypt import Bcrypt
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv
from datetime import date


load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db_path = os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)
bycrypt = Bcrypt(app)


"""
Crée une Instance LoginManager() : 
    -garder les utilisateur connecter
    - Protéger certaine route avec @login_required
    - Charger les utilisateur Automatiquement avec leur ID
    
"""
login_manager = LoginManager()

"""
 Si un utilisateur essaye d'accéder a une route @login_required
 - Le dirige vers la route login
"""
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


"""
    - Créé la table User pour l'utilisateur avec plusieurs tache 
    -> (un utilisateur peut avoir une ou plusieurs taches)
"""


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(100), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    habits = db.relationship("Habit", backref="user", lazy=True)


"""
    - Créé la table Habit pour une habitude crée par l'utilisateur
    -> user_id clé étranger vers user.id
"""


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    completions = db.relationship("Completion", backref="habit", lazy=True)


"""
    - Représente un jour où une habitude a été complétée
    -> date : jour où l’utilisateur a marqué l’habitude comme faite
    -> habit_id : clé étrangère vers l’habitude associée
"""


# Completion
class Completion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main", methods=["GET", "POST"])
@login_required
def main():
    if request.method == "POST":
        habit_name = request.form["habit_name"]
        new_habit = Habit(name=habit_name, user_id=current_user.id)
        db.session.add(new_habit)
        db.session.commit()
        flash("Nouvelle Habitude ajouter", "success")
        return redirect(url_for("main"))
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    today = date.today()
    completions = {c.habit_id for c in Completion.query.filter_by(date=today).all()}
    return render_template(
        "main.html", habits=habits, completions=completions, today=today
    )


@app.route("/delete_habit/<int:habit_id>")
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if habit.user_id == current_user.id:
        db.session.delete(habit)
        db.session.commit()
        flash("Habitude supprimée.", "info")
    return redirect(url_for("main"))


@app.route("/complete_habit/<int:habit_id>")
def complete_habit(habit_id):
    today = date.today()
    complete = Completion.query.filter_by(habit_id=habit_id, date=today).first()
    if complete:
        db.session.add(Completion(habit_id=habit_id, date=today))
        db.session.commit()
        flash("Habitude marquée comme faite.", "success")
    return redirect(url_for("main"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and bycrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main"))
        else:
            flash("Email ou mot de passe incorrect", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    flash("Déconnexion réussie.", "info")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        prenom = request.form["prenom"]
        nom = request.form["nom"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]
        if password != confirm:
            flash("Les mots de passe sont différents")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("Un compte existe déja avec cet email.")
            return redirect(url_for(register))

        # hasher le mot de passe
        hashed_pw = bycrypt.generate_password_hash(password).decode("utf-8")
        # Ajouter l'utilisateur a la base de données
        new_user = User(prenom=prenom, nom=nom, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Ton compte a bien été crée ! ", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
