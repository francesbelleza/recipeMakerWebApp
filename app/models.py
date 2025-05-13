from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from datetime import datetime

saved = db.Table('saved',
  db.Column('user_id',   db.Integer, db.ForeignKey('user.id'),   primary_key=True),
  db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)

recipe_tags = db.Table(
    'recipe_tags',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
    db.Column('tag_id',    db.Integer, db.ForeignKey('tag.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    recipes = db.relationship('Recipe', backref='author', lazy=True)
    ratings  = db.relationship('Rating',  backref='user',   lazy=True)    # ← add this
    comments = db.relationship('Comment', backref='user',   lazy=True)
    saved_recipes = db.relationship('Recipe', secondary=saved, backref=db.backref('saved_by', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def is_active(self):
        return True

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable = False) #cant be empty
    description = db.Column(db.Text, nullable = False)
    ingredients = db.Column(db.Text, nullable = False)
    instructions = db.Column(db.Text, nullable = False)
    created = db.Column(db.DateTime, default=datetime.utcnow) # use current time
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    ratings  = db.relationship('Rating',  backref='recipe', lazy=True)
    comments = db.relationship('Comment', backref='recipe', lazy=True)
    tags = db.relationship(
        'Tag',
        secondary=recipe_tags,
        back_populates='recipes',
        lazy='select'       
    )


class Rating(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    score     = db.Column(db.Integer, nullable=False)  # 1–5
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    body      = db.Column(db.Text, nullable=False)
    user_id   = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Tag(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    recipes = db.relationship(
      'Recipe',
      secondary=recipe_tags,
      back_populates='tags',
      lazy = 'dynamic'
    )