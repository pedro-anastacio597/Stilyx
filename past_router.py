from fastapi import FastAPI, HTTPException,APIRouter, Depends
from pydantic import BaseModel, EmailStr
from typing import List
import uuid
from datetime import datetime
from dependecis import sessao
from models import pasta, pasta_post, post, usuario
from verifications import verificar_post, verificar_usuario, verificar_pasta

past_router= APIRouter(tags=["past"])




class PastaEntrada(BaseModel):
    id_usuario: int
    nome: str
    descricao: str | None =None
    estado: str


@past_router.post("/pastas", status_code=201)
def criar_pasta(dados: PastaEntrada, session= Depends(sessao)):
    
    if not verificar_usuario(dados.id_usuario, session):
        raise HTTPException(status_code=404, detail="Usuario não existe")
    

    p= pasta(**dados.model_dump())

    session.add(p)
    session.commit()
    session.refresh(p)

    return p


@past_router.post("/pastas/{id_pasta}/add/{id_post}", status_code=200)
def adicionar_post(id_pasta: int, id_post:int, session= Depends(sessao)):

    if not verificar_pasta(id_pasta, session):
        raise HTTPException(status_code=404, detail="pasta não existe")
    
    if not verificar_post(id_post, session):
        raise HTTPException(status_code=404, detail="post não existe")
    
    p= pasta_post(id_pasta=id_pasta, id_post=id_post)

    session.add(p)
    session.commit()
    session.refresh(p)

    return p