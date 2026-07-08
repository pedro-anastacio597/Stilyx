from fastapi import FastAPI, HTTPException,APIRouter, Depends
from pydantic import BaseModel, EmailStr
from dependecis import sessao
from database import Post, Usuario, Categoria, Pasta, Denuncia, Curtida
    
def verificar_usuario(id_usuario: int, session):
    user= session.query(Usuario).filter(Usuario.id == id_usuario).first()
    
    return user
    
def verificar_post(id_post: int, session):
    post= session.query(Post).filter(Post.id == id_post).first()

    return post
    
def verificar_categoria(nome_categoria: list, session):
    categoria= session.query(Categoria).filter(Categoria.nome.in_(nome_categoria)).all()
    

    return len(categoria) == len(nome_categoria)

def verificar_pasta(id_pasta: int, session):
    pasta= session.query(Pasta).filter(Pasta.id == id_pasta).first()

    return pasta

def verificar_denuncia(id_denuncia: int, session):
    denuncia= session.query(Denuncia).filter(Denuncia.id == id_denuncia).first()

    return denuncia

def verificar_curtida(id_post, id_usuario, session):
    Curti= session.query(Curtida).filter(Curtida.id_post == id_post, Curtida.id_usuario == id_usuario).first()

    return Curti

def verificar_excluir(id_usuario: int, user: Usuario, session):
    
    if user.admin == False and user.id != id_usuario:
        raise HTTPException(status_code=400, detail="Não é possivél realizar está ação")
    else:
        return True
    
