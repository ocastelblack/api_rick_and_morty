from flask import flash, Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user, logout_user
from .models import Task
from .forms import TaskForm
from . import db
import requests

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('main.task_list'))

@main.route('/tasks')
@login_required
def task_list():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)

    tasks_query = Task.query.filter(Task.user_id == current_user.id)

    if query:
        tasks_query = tasks_query.filter(Task.title.ilike(f'%{query}%'))

    pagination = tasks_query.order_by(Task.due_date.asc()).paginate(page=page, per_page=5)
    tasks = pagination.items

    # Cargar personajes asociados
    characters_map = {}
    for task in tasks:
        if task.character_id:
            response = requests.get(f'https://rickandmortyapi.com/api/character/{task.character_id}')
            if response.status_code == 200:
                characters_map[task.id] = response.json()

    return render_template('task_list.html', tasks=tasks, pagination=pagination, characters_map=characters_map, query=query)

@main.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def task_create():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            status=form.status.data,
            user_id=current_user.id,
            character_id=form.character_id.data
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('main.task_list'))
    return render_template('task_form.html', form=form, edit=False, character=None)

@main.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def task_edit(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return "Acceso no autorizado", 403

    form = TaskForm(obj=task)

    # Cargar personaje asignado
    character_data = None
    if task.character_id:
        response = requests.get(f"https://rickandmortyapi.com/api/character/{task.character_id}")
        if response.status_code == 200:
            character_data = response.json()

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.status = form.status.data
        task.character_id = form.character_id.data
        db.session.commit()
        return redirect(url_for('main.task_list'))

    return render_template('task_form.html', form=form, edit=True, character=character_data)

@main.route('/tasks/delete/<int:task_id>')
@login_required
def task_delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return "Acceso no autorizado", 403
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.task_list'))

@main.route('/characters')
@login_required
def characters():
    page = request.args.get('page', 1, type=int)
    name = request.args.get('name', '')
    task_id = request.args.get('task_id', type=int)  # Para volver a editar si se desea

    url = f'https://rickandmortyapi.com/api/character/?page={page}'
    if name:
        url += f"&name={name}"

    response = requests.get(url)
    if response.status_code != 200:
        characters = []
        info = {'pages': 0, 'next': None, 'prev': None}
    else:
        data = response.json()
        characters = data['results']
        info = data['info']

    return render_template('characters.html', characters=characters, info=info, page=page, name=name, task_id=task_id)

@main.route('/tasks/assign_character/<int:character_id>')
@login_required
def assign_character(character_id):
    task_id = request.args.get('task_id', type=int)
    if not task_id:
        flash("Tarea no especificada.")
        return redirect(url_for('main.task_list'))

    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return "No autorizado", 403

    task.character_id = character_id
    db.session.commit()
    flash("Personaje asignado a la tarea.")
    return redirect(url_for('main.task_edit', task_id=task.id))

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for('auth.login'))