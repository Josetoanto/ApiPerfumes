from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.modules.auth.router import router as auth_router
from app.modules.perfumes.router import router as perfume_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Perfume Inventory API",
    description="API para gestionar usuarios y perfumes con autenticación JWT",
    version="1.0.0",
    contact={
        "name": "Equipo de Desarrollo",
        "email": "soporte@perfumeapi.com",
    }
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto a dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def global_exception_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={"error_code": "SERVER_ERROR", "message": "Error interno del servidor"}
        )

# Routers
app.include_router(auth_router)
app.include_router(perfume_router)

# Endpoint de healthcheck
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "message": "API funcionando correctamente"}
