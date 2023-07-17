from fastapi import FastAPI, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas import UserCreate, User
from models import Usuarios
from database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Configura el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes de todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todas las cabeceras
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/usuarios")
def get_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuarios).all()
    return usuarios

@app.post("/usuarios", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = Usuarios(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        if 'cedula' in str(e.orig):
            raise HTTPException(status_code=400, detail="Cédula ya registrada")
        elif 'telefono' in str(e.orig):
            raise HTTPException(status_code=400, detail="Número de teléfono ya registrado")
        elif 'email' in str(e.orig):
            raise HTTPException(status_code=400, detail="Correo electrónico ya registrado")
        else:
            raise HTTPException(status_code=400, detail="Error en los datos proporcionados")
    except ValidationError as v:
        raise HTTPException(status_code=400, detail=str(v))

@app.get("/usuarios/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(Usuarios).filter(Usuarios.Id_usuario == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/usuarios/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(Usuarios).filter(Usuarios.Id_usuario == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        if 'cedula' in str(e.orig):
            raise HTTPException(status_code=400, detail="Cédula ya registrada")
        elif 'telefono' in str(e.orig):
            raise HTTPException(status_code=400, detail="Número de teléfono ya registrado")
        elif 'email' in str(e.orig):
            raise HTTPException(status_code=400, detail="Correo electrónico ya registrado")
        else:
            raise HTTPException(status_code=400, detail="Error en los datos proporcionados")
    except ValidationError as v:
        raise HTTPException(status_code=400, detail=str(v))

@app.delete("/usuarios/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(Usuarios).filter(Usuarios.Id_usuario == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}
