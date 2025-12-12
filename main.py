from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = FastAPI()

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração do banco de dados
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'YOUR_PASSWORD_HERE',  # ← Usuário precisa configurar
    'database': 'todo_db'
}

# Modelo Pydantic para validação
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Função para conectar ao banco
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# Criar tabela se não existir
def init_db():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Banco de dados inicializado!")

# Inicializar banco ao startar
@app.on_event("startup")
async def startup():
    init_db()

# ROTAS DA API

@app.get("/")
def read_root():
    return {"message": "API de Tarefas está rodando!"}

# CREATE - Criar nova tarefa
@app.post("/tasks")
def create_task(task: Task):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco")
    
    cursor = conn.cursor()
    query = "INSERT INTO tasks (title, description, completed) VALUES (%s, %s, %s)"
    cursor.execute(query, (task.title, task.description, task.completed))
    conn.commit()
    
    task_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return {"id": task_id, "message": "Tarefa criada com sucesso!"}

# READ - Listar todas as tarefas
@app.get("/tasks")
def get_tasks():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco")
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return {"tasks": tasks}

# READ - Buscar tarefa por ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco")
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    return task

# UPDATE - Atualizar tarefa
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco")
    
    cursor = conn.cursor()
    
    # Verificar se tarefa existe
    cursor.execute("SELECT id FROM tasks WHERE id = %s", (task_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    # Atualizar campos fornecidos
    updates = []
    values = []
    
    if task.title is not None:
        updates.append("title = %s")
        values.append(task.title)
    if task.description is not None:
        updates.append("description = %s")
        values.append(task.description)
    if task.completed is not None:
        updates.append("completed = %s")
        values.append(task.completed)
    
    if updates:
        values.append(task_id)
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = %s"
        cursor.execute(query, values)
        conn.commit()
    
    cursor.close()
    conn.close()
    
    return {"message": "Tarefa atualizada com sucesso!"}

# DELETE - Deletar tarefa
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco")
    
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "Tarefa deletada com sucesso!"}