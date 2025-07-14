# Rick & Tasks

Una aplicación web hecha con Flask para gestionar tus tareas y asociarlas a personajes de Rick and Morty

## Funcionalidades

- Crear, editar y eliminar tareas.
- Asignar personajes de Rick and Morty a tareas.
- Buscador y paginación para tareas.
- Modal interactivo para elegir personajes.
- Autenticación de usuarios (login/logout).
- Interfaz responsiva con Bootstrap Darkly.

## Requisitos

- Python 3.8+
- Flask
- Flask-Login
- Flask-WTF
- requests
- SQLite (por defecto)

Instálalos con:

```bash
pip install -r requirements.txt

Instalación
Clona este repositorio:
git clone https://github.com/ocastelblack/api_rick_and_morty
cd rick-and-tasks

Crea la base de datos
sqlite3 app.db < schema.sql

Ejecuta la aplicación:
python app.py

Abre en tu navegador:
http://127.0.0.1:5000/login
