from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'task_management.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Table models
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    hashed_password = db.Column(db.Text, nullable=False)
    salt = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False, default='A')

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    task_name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    column_id = db.Column(db.Integer, db.ForeignKey('column.column_id'), nullable=False)
    due_date = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.Text, nullable=False)
    assignee = db.Column(db.Text, nullable=False)

    column = db.relationship('Column', backref=db.backref('tasks', lazy=True))

class Column(db.Model):
    column_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    column_name = db.Column(db.Text, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=False)
    status = db.Column(db.Text, nullable=False, default='A')

    board = db.relationship('Board', backref=db.backref('columns', lazy=True))

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    board_name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    status = db.Column(db.Text, nullable=False, default='A')

    user = db.relationship('User', backref=db.backref('boards', lazy=True))

class Assignee(db.Model):
    assignee_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    external_assignee = db.Column(db.Text)

    task = db.relationship('Task', backref=db.backref('assignees', lazy=True))
    user = db.relationship('User', backref=db.backref('assignees', lazy=True))

# Create database tables
db.create_all()

# Routes for application
@app.route('/')
def index():
    # Add logic to retrieve data from the database and render the Kanban board
    return render_template('index.html')

# Add more routes for CRUD operations, e.g., create_task, update_task, delete_task, etc.

if __name__ == '__main__':
    app.run(debug=True)
