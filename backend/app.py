import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql

db_host = os.getenv("DB_HOST","localhost")
db_user = os.getenv("DB_USER","root")
db_password = os.getenv("DB_PASSWORD","rootpass")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/task_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def create_database():
    try:
        connection = pymysql.connect(host=db_host, user=db_user, passwd=db_password)
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS task_db;")
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error creating database: {e}")

create_database()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'name': task.name,
        'description': task.description,
        'category': task.category,
        'priority': task.priority,
        'deadline': task.deadline
    } for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(
        name=data['name'],
        description=data['description'],
        category=data['category'],
        priority=data['priority'],
        deadline=data['deadline']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'}), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.json
    task.name = data.get('name', task.name)
    task.category = data.get('category', task.category)
    task.priority = data.get('priority', task.priority)
    task.deadline = data.get('deadline', task.deadline)
    task.description = data.get('description', task.description)
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
