from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

from routes.records import records_router
from routes.admin import admin_router
from routes.habits import habits_router
from fastapi.staticfiles import StaticFiles

from database.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API", version="1.0.0")

# Configurar Jinja2 para renderizar templates
templates = Jinja2Templates(directory="templates")

# Incluir as rotas
app.include_router(habits_router, tags=["Habits"])
app.include_router(records_router, tags=["Habits-records"])
app.include_router(admin_router, tags=["admin"])

# Rota para renderizar o template index.html
@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Inicializa o servidor
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
