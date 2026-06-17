from fastapi import FastAPI, HTTPException,APIRouter, Depends
from pydantic import BaseModel, EmailStr
from typing import List
import uuid
from datetime import datetime
from dependecis import sessao
from models import post, comentario,curtida, categoria, tag
from verifications import verificar_post, verificar_usuario, verificar_categoria, verificar_curtida
from sqlalchemy import or_

post_router= APIRouter(tags=["post"])



class PostEntrada(BaseModel):
    id_usuario: int
    imagem: str
    titulo: str
    descricao: str
    categoria: list[str]
    tag: list[str]

class Comentario(BaseModel):
    texto: str
    id_usuario: int

class Curtida(BaseModel):
    id_usuario: int


    @post_router.post("/posts", status_code=201)
    async def criar_post(dados: PostEntrada, session= Depends(sessao)):
        
        if not dados.imagem:
            raise HTTPException(status_code=404, detail="Selecione uma imagem")
        
        if not verificar_usuario(dados.id_usuario, session):
            raise HTTPException(status_code= 404, detail= "Uusario não existe") 
        
        if not verificar_categoria(dados.categoria, session):
            raise HTTPException(status_code=404, detail="Categorias inexistentes")
        
        categorias = session.query(categoria).filter(categoria.nome.in_(dados.categoria)).all()
        
        Tag_post=[]

        for nome_tag in dados.tag:
            t = session.query(tag).filter(tag.nome == nome_tag).first()

            if not t:
                t= tag(nome=nome_tag)
                session.add(t)
                session.flush()
                
            Tag_post.append(t)

        p= post(dados.imagem, dados.titulo, dados.descricao, dados.id_usuario)
        
        p.categorias.extend(categorias)
        p.tags.extend(Tag_post)

        session.add(p)
        session.commit()
        session.refresh(p)

        return p


@post_router.get("/posts", status_code=200)
async def listar_posts(session= Depends(sessao)):
    posts= session.query(post).all()

    return posts

@post_router.post("/posts/{id_post}/curtir", status_code=200)
async def curtir(id_post: int, id_usuario: int, session= Depends(sessao)):    
    
    if  verificar_curtida(id_post, id_usuario, session):
        raise HTTPException(status_code=404, detail="Curtida já existe")
    
    if not verificar_post(id_post, session):
        raise HTTPException(status_code=404, detail="Essa postagem não existe")
    else:
        if not verificar_usuario(id_usuario, session):
            raise HTTPException(status_code=404, detail="Usuario não existe")
        else:
            c= curtida(id_post= id_post, id_usuario= id_usuario)

            session.add(c)
            session.commit()
            session.refresh(c)
            return c


# comentar

@post_router.post("/posts/{id_post}/comentar")
def comentar(id_post: int, dados: Comentario, session=Depends(sessao)):

    if not dados.texto.strip():
        raise HTTPException(400, "comentário vazio")

    if not verificar_post(id_post,session):
        raise HTTPException(404, "post não existe")
    
    if not verificar_usuario(dados.id_usuario,session):
        raise HTTPException(status_code=404, detail="Usuario não existe")
    
    c= comentario(texto= dados.texto, id_usuario= dados.id_usuario, id_post= id_post)

    session.add(c)
    session.commit()
    session.refresh(c)

    return c


@post_router.post("/buscar", status_code=200)
async def buscar(q: str, session= Depends(sessao)):

    posts = (session.query(post).join(post.categorias).join(post.tags).filter(or_(categoria.nome.ilike(f"%{q}%"), tag.nome.ilike(f"%{q}%"))).distinct().all())
    return posts

@post_router.delete("/posts/{id_post}", status_code=204)
async def remover_post(id_post: int, session=Depends(sessao)):

    Post = verificar_post(id_post, session)

    if not Post:
        raise HTTPException(status_code=404, detail="post não existe")

    session.delete(Post)
    session.commit()

    return Post