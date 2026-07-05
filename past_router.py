from fastapi import FastAPI, HTTPException,APIRouter, Depends
from pydantic import BaseModel
from dependecis import sessao, verificar_token
from models import pasta, pasta_post, post, usuario
from verifications import verificar_post, verificar_usuario, verificar_pasta, verificar_excluir

past_router= APIRouter(tags=["past"], dependencies=[Depends(verificar_token)])




class PastaEntrada(BaseModel):
    id_usuario: int
    nome: str
    descricao: str | None =None
    estado: str


@past_router.post("/pasta", status_code=201)
def criar_pasta(dados: PastaEntrada, session= Depends(sessao), user: usuario= Depends(verificar_token)):
    
    if not verificar_usuario(dados.id_usuario, user, session):
        raise HTTPException(status_code=404, detail="Usuario não existe")
    

    p= pasta(**dados.model_dump())

    session.add(p)
    session.commit()
    session.refresh(p)

    return p


@past_router.post("/pasta/{id_pasta}/add/{id_post}", status_code=200)
def adicionar_post(id_pasta: int, id_post:int, session= Depends(sessao), user: usuario= Depends(verificar_token)):

    if not verificar_pasta(id_pasta, session):
        raise HTTPException(status_code=404, detail="pasta não existe")
    
    if not verificar_post(id_post, session):
        raise HTTPException(status_code=404, detail="post não existe")
    
    po= session.query(pasta).filter(pasta.id == id_post).first()

    if not po.usuario_id == user.id:
        raise HTTPException(status_code=400, detail="acao nao autorizada")

    
    p= pasta_post(id_pasta=id_pasta, id_post=id_post)

    session.add(p)
    session.commit()
    session.refresh(p)

    return p

@past_router.delete("/pasta/{id_pasta}/delete", status_code=200)
async def deletar_pasta(id_pasta, user: usuario = Depends(verificar_token), session= Depends(sessao)):

    Pasta= verificar_pasta(id_pasta, session)

    if not Pasta:
        raise HTTPException(status_code=400, detail="Pasta não existe")
    
    verificar_excluir(Pasta.id_usuario, user, session)

    
    session.delete(Pasta)
    session.commit()
    
    return Pasta