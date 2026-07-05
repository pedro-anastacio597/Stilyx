from fastapi import FastAPI, HTTPException,APIRouter, Depends
from pydantic import BaseModel
from dependecis import sessao, verificar_token
from models import post, usuario, denuncia
from verifications import verificar_usuario, verificar_denuncia, verificar_excluir, verificar_post

complaint_router= APIRouter(tags=["complaint"], dependencies=[Depends(verificar_token)])



class DenunciaEntrada(BaseModel):
    id_post: int | None = None
    id_alvo: int 
    motivo: str

@complaint_router.post("/denuncia", status_code=201)
def denunciar(dados: DenunciaEntrada, session= Depends(sessao), user: usuario= Depends(verificar_token)):


    u= verificar_usuario(dados.id_alvo, session)
    
    if not u:
        raise HTTPException(status_code=404, detail="Usuário denunciado não existe")

    
    d = denuncia(user.id,**dados.model_dump())

    session.add(d)
    session.commit()
    session.refresh(d)
    return d


@complaint_router.delete("/denuncia", status_code=200)
def apagardenuncia(id_denuncia: str, user: usuario= Depends(verificar_token), session= Depends(sessao)):
   
   d= verificar_denuncia(id_denuncia, session)
   if not d:
       raise HTTPException(status_code=404, detail="Denuncia não existe")
    
   verificar_excluir(d.id_usuario, user, session)
   
   session.delete(d)
   session.commit()

   return {"msg": "usuario deletado"}