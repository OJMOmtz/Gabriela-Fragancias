.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── producto.py
│   │   ├── cliente.py
│   │   ├── venta.py
│   │   └── inventario.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── usuario_schema.py
│   │   ├── producto_schema.py
│   │   ├── cliente_schema.py
│   │   └── venta_schema.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── crud_usuario.py
│   │   ├── crud_producto.py
│   │   ├── crud_cliente.py
│   │   └── crud_venta.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── usuario_router.py
│   │   ├── producto_router.py
│   │   ├── cliente_router.py
│   │   └── venta_router.py
│   └── services/
│       ├── __init__.py
│       ├── autenticacion.py
│       ├── validaciones.py
│       └── seguridad.py
├── requirements.txt
├── docker-compose.yml
└── Dockerfile

# requirements.txt
fastapi==0.109.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
pydantic==2.6.1
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.9
uvicorn==0.27.0.post1
alembic==1.13.1
email-validator==2.1.1

# main.py
from fastapi import FastAPI
from app.routers import usuario_router, producto_router, cliente_router, venta_router

app = FastAPI(
    title="Gabriela Fragancias",
    description="Sistema de Gestión de Perfumería",
    version="1.0.0"
)

# Registrar routers
app.include_router(usuario_router.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(producto_router.router, prefix="/productos", tags=["Productos"])
app.include_router(cliente_router.router, prefix="/clientes", tags=["Clientes"])
app.include_router(venta_router.router, prefix="/ventas", tags=["Ventas"])

# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://usuario:contraseña@localhost/gabriela_fragancias"
    SECRET_KEY: str = "tu_clave_secreta_super_segura"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()

# models/usuario.py
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class EstadoRegistro(enum.Enum):
    activo = "activo"
    inactivo = "inactivo"
    eliminado = "eliminado"

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    estado = Column(Enum(EstadoRegistro), default=EstadoRegistro.activo)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
