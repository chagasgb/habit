from fastapi import FastAPI
import uvicorn

from routes.records import records_router
from routes.admin import admin_router
from routes.habits import habits_router

from database import Base, engine
from models import Habit, HabitRecord  # Importar os modelos para garantir que Base.metadata saiba sobre eles

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API", version="1.0.0")

# Incluir as rotas
app.include_router(habits_router, tags=["Habits"])

app.include_router(records_router, tags=["Habits-records"])

app.include_router(admin_router, tags=["admin"])


# Inicializa o servidor
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)