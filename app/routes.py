from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_
from app import app, db
from app.models import User, Recipe, Rating, Comment
from app.forms import RegistrationForm, LoginForm, NewRecipe, SearchForm, RatingForm, CommentForm, DeleteForm, EditProfileForm
from statistics import mean



@app.route('/', methods=['GET','POST'])
def home():
    form    = SearchForm()
    recipes = Recipe.query.order_by(Recipe.created.desc()).all()

    if form.validate_on_submit():
        q = f"%{form.query.data}%"
        recipes = Recipe.query.filter(
            or_(
                Recipe.title.ilike(q),
                Recipe.ingredients.ilike(q)
            )
        ).all()

    return render_template('home.html', recipes=recipes, form=form)

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
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            author=current_user
        )
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe added!', 'success')
        return redirect(url_for('home'))
    return render_template('create_recipe.html', form=form)

#@app.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
#@login_required
#def delete_recipe(recipe_id):
#    recipe = Recipe.query.get_or_404(recipe_id)
#    if recipe.author != current_user:
#        flash('Not allowed.', 'danger')
#        return redirect(url_for('home'))
#    db.session.delete(recipe)
#    db.session.commit()
#    flash(f'Recipe "{recipe.title}" deleted.', 'success')
#    return redirect(url_for('home'))


@app.route('/recipe/<int:recipe_id>/edit', methods=['GET','POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        flash('Not allowed.', 'danger')
        return redirect(url_for('view_recipe', recipe_id=recipe.id))

    if request.method == 'POST':
        form = NewRecipe()
    else:
        form = NewRecipe(obj=recipe)

    if form.validate_on_submit():
        form.populate_obj(recipe)
        db.session.commit()
        flash('Recipe updated!', 'success')
        return redirect(url_for('view_recipe', recipe_id=recipe.id))

    return render_template('edit_recipe.html', form=form, recipe=recipe)


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


################## FOR DOM TO ADDDD ############################
@app.route('/recipe/<int:recipe_id>/save', methods=['POST'])
@login_required
def save_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe in current_user.saved_recipes:  # Fix: saved_recipes → saved_recipes
        flash('Recipe already saved.', 'info')
    else:
        current_user.saved_recipes.append(recipe)  # Fix here too
        db.session.commit()
        flash('Recipe saved successfully!', 'success')
    return redirect(url_for('view_recipe', recipe_id=recipe_id))



@app.route('/recipe/<int:recipe_id>/unsave', methods=['POST'])
@login_required
def unsave_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe in current_user.saved_recipes:  # Fix: Change `saved_recipes` to `saved_recipes`
        current_user.saved_recipes.remove(recipe)  # Fix: Change `saved_recipes` to `saved_recipes`
        db.session.commit()
        flash('Recipe removed from saved list.', 'success')
    else:
        flash('Recipe not in your saved list.', 'info')
    return redirect(url_for('view_recipe', recipe_id=recipe_id))



@app.route('/saved_recipes')
@login_required
def saved_recipes():
    return render_template('saved_recipes.html', recipes=current_user.saved_recipes)



@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    
    if form.validate_on_submit():
        if not check_password_hash(current_user.password, form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('edit_profile'))

        current_user.display_name = form.display_name.data
        current_user.email = form.email.data

        if form.new_password.data:
            current_user.password = generate_password_hash(form.new_password.data)

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))  # Redirect to the profile view (if you have one)

    return render_template('edit_profile.html', form=form)


@app.route('/recipes')
def all_recipes():
    recipes = Recipe.query.order_by(Recipe.title.asc()).all()
    return render_template('all_recipes.html', recipes=recipes)




