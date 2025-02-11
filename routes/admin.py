from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_db, Base, engine

admin_router = APIRouter(prefix="/admin", tags=["admin"])

@admin_router.delete("/reset-db")
async def reset_database(db: Session = Depends(get_db)):  
    try:
        # Apaga todas as tabelas usando o 'engine' correto
        Base.metadata.drop_all(bind=engine)
        
        # Recria todas as tabelas vazias
        Base.metadata.create_all(bind=engine)
        
        return {"message": "Banco de dados resetado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))