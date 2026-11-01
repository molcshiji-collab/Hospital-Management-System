# Hospital Management System

Intermediate Python OOP + MySQL command-line project.

## Features
- Patient CRUD: create, read, update and delete
- Doctor CRUD: create, read, update and delete
- Book and view appointments
- Update appointment status
- MySQL foreign keys and unique doctor appointment slots
- Parameterized SQL queries

## Requirements
- Python 3
- MySQL Server
- VS Code (recommended)

## Setup
1. Open MySQL Workbench and run `schema.sql`.
2. Open `config.py` and enter your MySQL host, username and password.
3. In the VS Code terminal, install dependencies:
   `pip install -r requirements.txt`
4. Run the application:
   `python main.py`

Appointment date format: `YYYY-MM-DD`
Appointment time format: `HH:MM:SS`

Use sample or fictional records for practice. This educational project is not intended for real patient records or clinical use.
