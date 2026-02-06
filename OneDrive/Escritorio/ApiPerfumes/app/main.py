from fastapi import FastAPI
from app.core.database import Base, engine
from app.modules.auth.router import router as auth_router
from app.modules.perfumes.router import router as perfume_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Perfume Inventory API")

app.include_router(auth_router)
app.include_router(perfume_router)
