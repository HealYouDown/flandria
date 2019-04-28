from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask_babel import gettext

from webapp import db
from webapp.auth.forms import LoginForm, RegisterForm
from webapp.auth.models import User
from webapp.planner.models import UserBuild

auth = Blueprint("auth", __name__, url_prefix="/auth")

@auth.route("/signin", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))

    form = LoginForm()

    if form.validate_on_submit():
        
        user = User.query.filter(User.username.ilike(form.username.data)).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.signin"))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        # check if url is safe, else redirect to home
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home.index')

        return redirect(next_page)

    return render_template("auth/signin.html", title=gettext("Sign In"), form=form)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Account was created successfully", "success")
        return redirect(url_for("auth.signin"))

    return render_template("auth/signup.html", title=gettext("Sign In"), form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@auth.route("/my-builds")
@login_required
def my_builds():
    builds = db.session.query(UserBuild).filter(UserBuild.user_id == current_user.id).order_by(UserBuild.stars_count.desc()).all()
    return render_template("auth/my_builds.html", title=gettext("My builds"), builds=builds)