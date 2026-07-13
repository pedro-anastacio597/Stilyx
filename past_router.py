from fastapi import FastAPI, HTTPException,APIRouter, Depends
from pydantic import BaseModel
from dependecis import sessao, verificar_token
from database import Pasta, PastaPost, Post, Usuario
from verifications import verificar_post, verificar_usuario, verificar_pasta, verificar_excluir
from models import PastaEntrada

past_router= APIRouter(tags=["past"], dependencies=[Depends(verificar_token)])


@past_router.post("/pasta", status_code=201)
def criar_pasta(dados: PastaEntrada, session= Depends(sessao), user: Usuario= Depends(verificar_token)):
    
    p= Pasta(nome=dados.nome, descricao= dados.descricao, estado= dados.estado, id_usuario= user.id)

    session.add(p)
    session.commit()
    session.refresh(p)

    return p


@past_router.post("/pasta/{id_pasta}/add/{id_post}", status_code=200)
def adicionar_post(id_pasta: int, id_post:int, session= Depends(sessao), user: Usuario= Depends(verificar_token)):

    pa = verificar_pasta(id_pasta, session)

    if not pa:
        raise HTTPException(status_code=404, detail="pasta não existe")
    
    if pa.id_usuario != user.id:
        raise HTTPException(status_code=400, detail="ação não é permitida")
    
    if not verificar_post(id_post, session):
        raise HTTPException(status_code=404, detail="post não existe")

    p= PastaPost(id_pasta=id_pasta, id_post=id_post)

    session.add(p)
    session.commit()
    session.refresh(p)

    return p

@past_router.delete("/pasta/{id_pasta}/delete", status_code=200)
async def deletar_pasta(id_pasta, user: Usuario = Depends(verificar_token), session= Depends(sessao)):

    Pasta= verificar_pasta(id_pasta, session)

    if not Pasta:
        raise HTTPException(status_code=400, detail="Pasta não existe")
    
    verificar_excluir(Pasta.id_usuario, user, session)

    
    session.delete(Pasta)
    session.commit()
    
    return {"mensagem": "Pasta removido com sucesso"}