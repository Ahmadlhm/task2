from fastapi import FastAPI, HTTPException
import sqlite3
from config import DB_PATH

app = FastAPI()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        salary REAL NOT NULL,
        hire_date TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

init_db()

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/employees")
def get_all():
    conn = connect_db()
    data = conn.execute("SELECT * FROM employees").fetchall()
    conn.close()
    return [dict(row) for row in data]

@app.get("/employees/{employee_id}")
def get_one(employee_id: int):
    conn = connect_db()
    row = conn.execute("SELECT * FROM employees WHERE employee_id=?", (employee_id,)).fetchone()
    conn.close()
    if row: return dict(row)
    raise HTTPException(status_code=404, detail="Employee not found")

@app.post("/employees")
def add_employee(employee: dict):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)",
                (employee["name"], employee["department"], employee["salary"], employee["hire_date"]))
    conn.commit()
    emp_id = cur.lastrowid
    conn.close()
    return {"employee_id": emp_id}

@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: dict):
    conn = connect_db()
    conn.execute("UPDATE employees SET name=?, department=?, salary=?, hire_date=? WHERE employee_id=?",
                 (employee["name"], employee["department"], employee["salary"], employee["hire_date"], employee_id))
    conn.commit()
    conn.close()
    return {"message": "Updated"}

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    conn = connect_db()
    conn.execute("DELETE FROM employees WHERE employee_id=?", (employee_id,))
    conn.commit()
    conn.close()
    return {"message": "Deleted"}



