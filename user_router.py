from fastapi import FastAPI, HTTPException,APIRouter, Depends
from pydantic import BaseModel, EmailStr
from typing import List
import uuid
from datetime import datetime
from models import usuario
from dependecis import sessao

user_router=APIRouter(tags=["user"])

class UsuarioEntrada(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    foto: str | None = None
    bio: str  | None = None


@user_router.get("/usarios", status_code=200)
async def listarusuarios(session= Depends(sessao)):
    Usuario= session.query(usuario).all()
    return Usuario

@user_router.post("/usuario", status_code=201)
async def cadastro(dados: UsuarioEntrada, session= Depends(sessao)):
    
    Email= session.query(usuario).filter(usuario.email == dados.email).first()

    if Email:
        raise HTTPException(409, "email já cadastrado!")
    
    u= usuario(**dados.model_dump())

    session.add(u)
    session.commit()
    session.refresh(u)

    return u
    

@user_router.post("/login", status_code=200)
async def login(email: str, senha: str, session= Depends(sessao)):
    user= session.query(usuario).filter(usuario.email == email, usuario.senha == senha).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Email ou senha invalidos")
    
    session.refresh(user)
    return user

@user_router.patch("/usuario/{id}", status_code=200)
async def editar_perfil(id: int, bio:str, foto:str, session= Depends(sessao)):

    user= session.query(usuario).filter(usuario.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao existe")
    
    user.bio=bio
    user.foto= foto

    session.commit()
    session.refresh(user)

    return user

@user_router.delete("/usuario/{id}", status_code=200)
async def removerusuario(id: int, session=Depends(sessao)):
    user= session.query(usuario).filter(usuario.id == id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail= "Usuario não existe")
    
    session.delete(user)
    session.commit()

    return user