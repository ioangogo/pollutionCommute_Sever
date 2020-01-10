from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        Username = request.form.get("username")
        print(Username)
        password = request.form.get("password")
        user = User.query.filter_by(username=Username).first()
        print(user)
        if not user and check_password_hash(user.password, password):
            return redirect(url_for('auth.login'))
        else:
            login_user(user)
            return redirect(url_for('views.sensors'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    elif request.method == 'POST':
        Username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=Username).first()
        print(user)
        if user:
            flash('User already exists')
            return redirect(url_for('auth.signup'))
        else:
            new_user = User(username=Username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))