from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import User, Recipe
from app.forms import RegistrationForm, LoginForm, NewRecipe
from flask_login import login_user, current_user, logout_user, login_required

bp = Blueprint('main', __name__)

@bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        flash('Login failed.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@bp.route('/recipe/new', methods=['GET','POST'])
@login_required
def new_recipe():
    form = NewRecipe()
    if form.validate_on_submit():
        recipe = Recipe(title=form.title.data,
                        description=form.description.data,
                        ingredients=form.ingredients.data,
                        instructions=form.instructions.data,
                        author=current_user)
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe added!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_recipe.html', form=form)

@bp.route('/')
def home():
    recipes = Recipe.query.all()
    return render_template('home.html', recipes=recipes)
