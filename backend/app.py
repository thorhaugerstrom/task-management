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
# Task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(
        task_name=data['task_name'],
        description=data['description'],
        column_id=data['column_id'],
        due_date=data['due_date'],
        created_date=data['created_date'],
        assignee=data['assignee']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created successfully", "task_id": new_task.task_id}), 201

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    task_list = [{"task_id": task.task_id, "task_name": task.task_name, "description": task.description,
                  "column_id": task.column_id, "due_date": task.due_date, "created_date": task.created_date,
                  "assignee": task.assignee} for task in tasks]
    return jsonify({"tasks": task_list})


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify({"task_id": task.task_id, "task_name": task.task_name, "description": task.description,
                    "column_id": task.column_id, "due_date": task.due_date, "created_date": task.created_date,
                    "assignee": task.assignee})

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    task.task_name = data.get('task_name', task.task_name)
    task.description = data.get('description', task.description)
    task.column_id = data.get('column_id', task.column_id)
    task.due_date = data.get('due_date', task.due_date)
    task.assignee = data.get('assignee', task.assignee)
    db.session.commit()
    return jsonify({"message": "Task updated successfully"})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})

# User
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        email=data['email'],
        hashed_password=data['hashed_password'],
        salt=data['salt'],
        status=data.get('status', 'A')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "user_id": new_user.user_id}), 201

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = [{"user_id": user.user_id, "email": user.email, "status": user.status} for user in users]
    return jsonify({"users": user_list})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({"user_id": user.user_id, "email": user.email, "status": user.status})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.email = data.get('email', user.email)
    user.hashed_password = data.get('hashed_password', user.hashed_password)
    user.salt = data.get('salt', user.salt)
    user.status = data.get('status', user.status)
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
