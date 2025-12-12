# 📝 Sistema de Registro de Tarefas

Aplicação fullstack para gerenciamento de tarefas com operações CRUD completas (Create, Read, Update, Delete).

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **FastAPI** - Framework web moderno e rápido
- **MySQL** - Banco de dados relacional
- **Uvicorn** - Servidor ASGI

### Frontend
- **HTML5** - Estrutura da página
- **CSS3** - Estilização com gradientes e animações
- **JavaScript** - Comunicação com a API (Fetch API)

## 📁 Estrutura do Projeto

```
Registro_Tarefas/
├── main.py          # Backend FastAPI com rotas da API
├── index.html       # Interface do usuário
└── README.md        # Este arquivo
```

## ⚙️ Funcionalidades

### Backend (`main.py`)
- **POST /tasks** - Criar nova tarefa
- **GET /tasks** - Listar todas as tarefas
- **GET /tasks/{id}** - Buscar tarefa específica
- **PUT /tasks/{id}** - Atualizar tarefa
- **DELETE /tasks/{id}** - Deletar tarefa
- Conexão com MySQL usando `mysql-connector-python`
- Validação de dados com Pydantic
- CORS habilitado para comunicação com frontend

### Frontend (`index.html`)
- Formulário para criar novas tarefas
- Lista dinâmica de tarefas
- Botões para marcar como concluída/reabrir
- Botão para deletar tarefas
- Design responsivo com gradientes
- Alertas de sucesso/erro
- Atualização automática da lista

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- MySQL instalado e rodando
- Navegador web moderno

### 1. Configurar o Banco de Dados

Abra o MySQL e execute:

```sql
CREATE DATABASE todo_db;
```

### 2. Configurar o Backend

**Instalar dependências:**

```bash
pip install fastapi uvicorn mysql-connector-python pydantic
```

**Configurar credenciais do MySQL:**

Abra o arquivo `main.py` e altere as configurações na linha 19-24:

```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'SUA_SENHA_AQUI',  # ← Coloque sua senha do MySQL
    'database': 'todo_db'
}
```

**Rodar o servidor:**

```bash
uvicorn main:app --reload
```

O backend estará disponível em `http://localhost:8000`

### 3. Abrir o Frontend

Simplesmente abra o arquivo `index.html` no seu navegador (duplo clique ou arraste para o navegador).

## 📡 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Verificar se API está rodando |
| POST | `/tasks` | Criar nova tarefa |
| GET | `/tasks` | Listar todas as tarefas |
| GET | `/tasks/{id}` | Buscar tarefa por ID |
| PUT | `/tasks/{id}` | Atualizar tarefa |
| DELETE | `/tasks/{id}` | Deletar tarefa |

### Documentação Interativa

Acesse `http://localhost:8000/docs` para ver a documentação automática (Swagger UI) da API.

## 🗄️ Estrutura do Banco de Dados

**Tabela: `tasks`**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INT | Identificador único (auto increment) |
| title | VARCHAR(255) | Título da tarefa |
| description | TEXT | Descrição detalhada (opcional) |
| completed | BOOLEAN | Status de conclusão |
| created_at | TIMESTAMP | Data/hora de criação |

## 💡 Como Funciona

1. O **backend** (FastAPI) recebe requisições HTTP e processa as operações no banco de dados
2. O **frontend** (HTML/CSS/JS) faz requisições para a API usando `fetch()`
3. Os dados são enviados e recebidos no formato JSON
4. O MySQL armazena permanentemente todas as tarefas

## 🔧 Solução de Problemas

### Erro: "No module named 'fastapi'"
```bash
pip install fastapi uvicorn mysql-connector-python pydantic
```

### Erro: "Unknown MySQL server host"
- Verifique se o MySQL está rodando
- Use `127.0.0.1` ao invés de `localhost`
- Confirme que a porta é `3306`

### Frontend não conecta com backend
- Certifique-se que o backend está rodando em `http://localhost:8000`
- Verifique o console do navegador (F12) para erros
- Confirme que o CORS está habilitado no backend

## 📝 Licença

Este é um projeto educacional livre para uso e modificação.

## 👨‍💻 Autor

Desenvolvido como projeto de aprendizado fullstack.
