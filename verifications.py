from fastapi import FastAPI, HTTPException,APIRouter, Depends
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from dependecis import sessao
from models import post, usuario, categoria, pasta, denuncia, curtida
    
def verificar_usuario(id_usuario: int, user:usuario, session):
    if user.id != id_usuario:
        raise HTTPException(status_code=400, detail="Ação bloqueada")
    
    return user
    
def verificar_post(id_post: int, session):
    Post= session.query(post).filter(post.id == id_post).first()

    return Post
    
def verificar_categoria(nome_categoria: list, session):
    Categoria= session.query(categoria).filter(categoria.nome.in_(nome_categoria)).all()
    

    return len(Categoria) == len(nome_categoria)

def verificar_pasta(id_pasta: int, session):
    Pasta= session.query(pasta).filter(pasta.id == id_pasta).first()

    return Pasta

def verificar_denuncia(id_denuncia: int, session):
    Denuncia= session.query(denuncia).filter(denuncia.id == id_denuncia).first()

    return Denuncia

def verificar_curtida(id_post, id_usuario, session):
    Curti= session.query(curtida).filter(curtida.id_post == id_post, curtida.id_usuario == id_usuario)

    return Curti

def verificar_excluir(id_usuario: int, user: usuario, session):
    
    if user.admin == False and user.id != id_usuario:
        raise HTTPException(status_code=400, detail="Não é possivél realizar está ação")
    else:
        return True
    
