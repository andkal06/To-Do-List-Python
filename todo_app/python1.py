from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=False)
    date_completed = db.Column(db.DateTime)
    note = db.Column(db.String(500))
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    filter_date = request.args.get('filter_date')
    todos = Todo.query.all()
    
    if filter_date:
        filter_date = datetime.strptime(filter_date, '%Y-%m-%d').date()
        ongoing_todos = [todo for todo in todos if not todo.completed and todo.deadline.date() == filter_date]
        completed_todos = [todo for todo in todos if todo.deadline and todo.deadline.date() == filter_date]
    else:
        ongoing_todos = sorted((todo for todo in todos if not todo.completed), key=lambda x: x.deadline)
        completed_todos = sorted((todo for todo in todos if todo.completed), key=lambda x: x.deadline or datetime.min)

    current_time = datetime.utcnow()
    for todo in ongoing_todos:
        if todo.deadline < current_time:
            todo.status = "Lewat Deadline" 
        else:
            todo.status = "Belum Selesai"

    completed_count = len(completed_todos)
    total_count = len(ongoing_todos) + len(completed_todos)

    return render_template('index.html', ongoing_todos=ongoing_todos, 
                                         completed_todos=completed_todos,
                                         completed_count=completed_count, 
                                         total_count=total_count, 
                                         filter_date=filter_date)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    deadline = request.form.get('deadline')
    note = request.form.get('note')

    try:
        deadline_date = datetime.strptime(deadline, '%Y-%m-%dT%H:%M')
    except ValueError:
        return "Error: Invalid date format", 400

    new_todo = Todo(task=task, deadline=deadline_date, note=note)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>')
def complete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        todo.completed = True
        todo.date_completed = datetime.utcnow()
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/restore/<int:todo_id>')
def restore(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        todo.completed = False
        todo.date_completed = None
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)