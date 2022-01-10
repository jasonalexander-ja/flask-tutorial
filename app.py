from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import aiohttp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'

@app.route('/', methods=['POST', 'GET'])
async def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_todo = Todo(content=task_content)
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue returning your task'
    else:
        poke_name = ''
        async with aiohttp.ClientSession() as session:

            pokemon_url = 'https://pokeapi.co/api/v2/pokemon/151'
            async with session.get(pokemon_url) as resp:
                pokemon = await resp.json()
                poke_name = pokemon['name']
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks = tasks, poke_name = poke_name)

@app.route('/delete/<int:id>')
async def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a prblem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating your task"
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug = True)
