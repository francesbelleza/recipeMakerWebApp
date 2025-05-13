from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_
from app import app, db
from app.models import User, Recipe, Rating, Comment, Tag
from app.forms import RegistrationForm, LoginForm, NewRecipe, SearchForm, RatingForm, CommentForm, DeleteForm, EditProfileForm
from statistics import mean

@app.route('/', methods=['GET','POST'])
def home():
    form          = SearchForm()
    tag_name      = request.args.get('tag')     # ?tag=Vegan
    selected_tag  = tag_name

    # start from the base Recipe.query
    query = Recipe.query

    if form.validate_on_submit():
        q = f"%{form.query.data}%"
        query = query.filter(
            or_(
                Recipe.title.ilike(q),
                Recipe.ingredients.ilike(q)
            )
        )
    elif tag_name:
        # join through the secondary table to Tag
        query = (
            query
            .join(Recipe.tags)
            .filter(Tag.name == tag_name)
        )

    # finally order & fetch
    recipes  = query.order_by(Recipe.created.desc()).all()
    all_tags = Tag.query.order_by(Tag.name).all()

    return render_template(
        'home.html',
        recipes=recipes,
        form=form,
        all_tags=all_tags,
        selected_tag=selected_tag
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already in use.', 'warning')
            return redirect(url_for('register'))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        flash('Login failed. Check credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/recipe/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = NewRecipe()

    form.tags.choices = [(t.id, t.name) for t in Tag.query.order_by(Tag.name)]

    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            author=current_user
        )

        recipe.tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()

        db.session.add(recipe)
        db.session.commit()
        flash('Recipe added!', 'success')
        return redirect(url_for('home'))

    return render_template('create_recipe.html', form=form)


@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe       = Recipe.query.get_or_404(recipe_id)
    rating_form  = RatingForm()
    comment_form = CommentForm()
    delete_form = DeleteForm()

    # compute avg if there are any ratings
    ratings = [r.score for r in recipe.ratings]
    avg_rating = mean(ratings) if ratings else None

    return render_template(
        'view_recipe.html',
        recipe=recipe,
        rating_form=rating_form,
        comment_form=comment_form,
        delete_form=delete_form,
        avg_rating=avg_rating
    )


@app.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        abort(403)

    form = NewRecipe(obj=recipe)
    form.tags.choices = [(t.id, t.name) for t in Tag.query.order_by(Tag.name)]

    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data

        recipe.tags = (
            Tag.query
            .filter(Tag.id.in_(form.tags.data))
            .all()
        )

        db.session.commit()
        flash('Recipe updated!', 'success')
        return redirect(url_for('view_recipe', recipe_id=recipe.id))

    return render_template('edit_recipe.html', form=form, recipe=recipe)


@app.route("/search", methods=["GET","POST"])
def search():
    form = SearchForm()
    recipes = []
    if form.validate_on_submit():
        q = f"%{form.query.data}%"
        recipes = Recipe.query.filter(
            db.or_(
              Recipe.title.ilike(q),
              Recipe.ingredients.ilike(q)
            )
        ).all()
    return render_template("home.html", recipes=recipes, form=form)

@app.route("/recipe/<int:recipe_id>/rate", methods=["POST"])
@login_required
def rate(recipe_id):
    form = RatingForm()
    if form.validate_on_submit():
        # delete old rating by this user, if any
        old = Rating.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
        if old:
            db.session.delete(old)
        new = Rating(score=form.score.data, user_id=current_user.id, recipe_id=recipe_id)
        db.session.add(new)
        db.session.commit()
        flash("Thanks for your rating!", "success")
    return redirect(url_for("view_recipe", recipe_id=recipe_id))

@app.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        flash('Not allowed to delete this recipe.', 'danger')
        return redirect(url_for('home'))

    #needed so we can delete recipes
    Comment.query.filter_by(recipe_id=recipe.id).delete()
    Rating.query.filter_by(recipe_id=recipe.id).delete()

    db.session.delete(recipe)
    db.session.commit()

    flash('Recipe deleted.', 'success')
    return redirect(url_for('home'))

@app.route("/recipe/<int:recipe_id>/comment", methods=["POST"])
@login_required
def comment(recipe_id):
    form = CommentForm()
    if form.validate_on_submit():
        c = Comment(body=form.body.data, user_id=current_user.id, recipe_id=recipe_id)
        db.session.add(c)
        db.session.commit()
        flash("Comment posted!", "success")
    return redirect(url_for("view_recipe", recipe_id=recipe_id))

@app.route("/user/<int:user_id>")
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("profile.html", user=user)

@app.route('/profile/edit', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(
      username=current_user.username,
      email=current_user.email
    )
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email    = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('profile', user_id=current_user.id))
    return render_template('edit_profile.html', form=form)

@app.route('/recipe/<int:recipe_id>/save', methods=['POST'])
@login_required
def save_recipe(recipe_id):
    r = Recipe.query.get_or_404(recipe_id)
    if r in current_user.saved_recipes:
        current_user.saved_recipes.remove(r)
        flash('Removed from your saved recipes', 'info')
    else:
        current_user.saved_recipes.append(r)
        flash('Saved!', 'success')
    db.session.commit()
    return redirect(url_for('view_recipe', recipe_id=recipe_id))



