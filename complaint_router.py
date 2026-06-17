from fastapi import FastAPI, HTTPException,APIRouter, Depends
from pydantic import BaseModel, EmailStr
from typing import List
import uuid
from datetime import datetime
from dependecis import sessao
from models import post, usuario, denuncia
from verifications import verificar_usuario, verificar_denuncia

complaint_router= APIRouter(tags=["complaint"])



class DenunciaEntrada(BaseModel):
    id_usuario: int
    id_alvo: int
    motivo: str

@complaint_router.post("/denuncia", status_code=201)
def denunciar(dados: DenunciaEntrada, session= Depends(sessao)):

    if not verificar_usuario(dados.id_usuario, session):
        raise HTTPException(status_code=404, detail="Usuário que denuncia não existe")

    if not verificar_usuario(dados.id_alvo, session):
        raise HTTPException(status_code=404, detail="Usuario alvo não existe")
    
    d = denuncia(**dados.model_dump())

    session.add(d)
    session.commit()
    session.refresh(d)
    return d


@complaint_router.delete("/denuncia", status_code=200)
def apagardenuncia(id_denuncia: str, session= Depends(sessao)):
   
   d= verificar_denuncia(id_denuncia, session)
   if not d:
       raise HTTPException(status_code=404, detail="Denuncia não existe")
   
   session.delete(d)
   session.commit()

   return {"msg": "usuario deletado"}