from sqlalchemy.orm import sessionmaker
from database import db, Usuario
from sqlalchemy.orm import session
from database import Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWSError
from config import SECRET_KEY, ALGORITHM, OAuth2_schema

def sessao():
    try:
        session= sessionmaker(bind=db)
        Session= session()
        yield Session
    finally:
        Session.close()


def verificar_token(token: str =Depends(OAuth2_schema), Session: session= Depends(sessao)):
    print("ENTROU NO VERIFICAR TOKEN")
    print("TOKEN RECEBIDO:", token)
    try:
        dict_info= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario= int(dict_info["sub"])
    except Exception as e:
        print("ERRO JWT:", e)
        raise HTTPException(
            status_code=401,
            detail="Token invalido"
        )
    
    user= Session.query(Usuario).filter(Usuario.id == id_usuario).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    
    return user

