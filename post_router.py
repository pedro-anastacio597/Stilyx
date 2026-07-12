from fastapi import FastAPI, HTTPException,APIRouter, Depends
from pydantic import BaseModel, EmailStr
from typing import List
from dependecis import sessao, verificar_token
from database import Post, Comentario, Curtida, Categoria, Tag, Usuario, PostCategoria, PostTag
from verifications import verificar_post, verificar_usuario, verificar_categoria, verificar_curtida, verificar_excluir
from sqlalchemy import or_
from models import PostEntrada, comentario

post_router= APIRouter(tags=["post"], dependencies=[Depends(verificar_token)])


@post_router.post("/posts", status_code=201)
async def criar_post(dados: PostEntrada, user: Usuario= Depends(verificar_token),session= Depends(sessao)):

    categorias=[]
    if not dados.imagem:
        raise HTTPException(status_code=404, detail="Selecione uma imagem")
    
    if dados.categoria:
        if not verificar_categoria(dados.categoria, session):
            raise HTTPException(status_code=404, detail="Categorias inexistentes")
    
        categorias = session.query(Categoria).filter(Categoria.nome.in_(dados.categoria)).all()
    
    Tag_post=[]
    if dados.tag:
        for nome_tag in dados.tag:
            t = session.query(Tag).filter(Tag.nome == nome_tag).first()

            if not t:
                t= Tag(nome=nome_tag)
                session.add(t)
                session.flush()
                
            Tag_post.append(t)

    p= Post(dados.imagem, dados.titulo, dados.descricao, user.id)
    session.add(p)
    session.flush()

    if dados.tag:
        for tag in Tag_post:
            pt=PostTag(p.id, tag.id)

            session.add(pt)
    if dados.categoria:    
        for categorias in dados.categoria:
            c= session.query(Categoria).filter(Categoria.nome == categorias).first()     
            pc=PostCategoria(p.id, c.id)

            session.add(pc)


    
    session.commit()
    session.refresh(p)

    return p


@post_router.get("/posts", status_code=200)
async def listar_posts(session= Depends(sessao)):
    posts= session.query(Post).all()

    return posts

@post_router.post("/posts/{id_post}/curtir", status_code=200)
async def curtir( id_post: int, user: Usuario= Depends(verificar_token), session= Depends(sessao)):    
    
    if verificar_curtida(id_post, user.id, session):
        raise HTTPException(status_code=404, detail="Curtida já existe")
    
    if not verificar_post(id_post, session):
        raise HTTPException(status_code=404, detail="Essa postagem não existe")
    
    c= Curtida(id_post= id_post, id_usuario= user.id)

    session.add(c)
    session.commit()
    session.refresh(c)
    return c


# comentar

@post_router.post("/posts/{id_post}/comentar")
def comentar(id_post: int, dados: comentario, session=Depends(sessao), user: Usuario= Depends(verificar_token)):

    if not dados.texto.strip():
        raise HTTPException(400, "comentário vazio")

    if not verificar_post(id_post,session):
        raise HTTPException(404, "post não existe")
        
    c= Comentario(texto=dados.texto, id_usuario=user.id, id_post=dados.id_post)

    session.add(c)
    session.commit()
    session.refresh(c)
 
    return c


@post_router.post("/buscar", status_code=200)
async def buscar(q: str, session= Depends(sessao)):

    posts = (session.query(Post).outerjoin(Post.post_categoria).outerjoin(Post.post_tag).outerjoin(PostCategoria.categoria).outerjoin(PostTag.tag).filter(or_(Post.descricao.ilike(f"%{q}%"), Post.titulo.ilike(f"%{q}%") ,Categoria.nome.ilike(f"%{q}%"), Tag.nome.ilike(f"%{q}%"))).distinct().all())
    return posts

@post_router.patch("/post/{id_post}/atualizarpost", status_code=200)
async def editrarpost(id_post: int, descricao: str, titulo: str, session= Depends(sessao)):

    Post= verificar_post(id_post, session)

    if not Post:
        raise HTTPException(status_code=404, detail="Post não existe")
    
    Post.descricao = descricao
    Post.titulo = titulo

    session.commit()
    session.refresh(Post)
    
    return  Post

@post_router.delete("/posts/{id_post}", status_code=200)
async def remover_post(id_post: int, session=Depends(sessao), user: Usuario = Depends(verificar_token)):

    post = verificar_post(id_post, session)

    if not post:
        raise HTTPException(status_code=404, detail="post não existe")
    
    verificar_excluir(post.id_usuario, user, session)


    session.delete(post)
    session.commit()

    return {"mensagem": "Post removido com sucesso"}