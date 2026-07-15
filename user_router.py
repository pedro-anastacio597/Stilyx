from fastapi import FastAPI, HTTPException,APIRouter, Depends
from datetime import timedelta, datetime, timezone
from dependecis import sessao, verificar_token
from config import bcrypt_context, ALGORITHM, ACESS_TOKEN_EXPIREM,SECRET_KEY
from jose import jwt, JWSError
from fastapi.security import OAuth2PasswordRequestForm
from verifications import verificar_excluir
from datetime import datetime, timedelta, timezone
from jose import jwt
from models import UsuarioEntrada
from database import Usuario

user_router=APIRouter(tags=["user"])

def criar_token(id_usuario, data_exp=timedelta(minutes=int(ACESS_TOKEN_EXPIREM))):
    data_expiracao = datetime.now(timezone.utc) + data_exp

    dict_info = {
        "sub": str(id_usuario),
        "exp": data_expiracao
    }

    token = jwt.encode(
        dict_info,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

@user_router.get("/usarios", status_code=200)
async def listarusuarios(session= Depends(sessao)):
    usuarios= session.query(Usuario).all()
    return usuarios

@user_router.get("/usuario", status_code=200)
async def buscarusuario(id_usuario: int, session= Depends(sessao)):
    user= session.query(Usuario).filter(Usuario.id == id_usuario).first()
    return user

@user_router.post("/usuario", status_code=201)
async def cadastro(dados: UsuarioEntrada, session= Depends(sessao)):
    
    Email= session.query(Usuario).filter(Usuario.email == dados.email).first()

    if Email:
        raise HTTPException(409, "email já cadastrado!")
    dados.senha= bcrypt_context.hash(dados.senha)
    
    u= Usuario(**dados.model_dump())

    session.add(u)
    session.commit()
    session.refresh(u)

    return u
    

@user_router.post("/login", status_code=200)
async def login(dadoos_formulario:OAuth2PasswordRequestForm = Depends() , session= Depends(sessao)):
    user= session.query(Usuario).filter(Usuario.email == dadoos_formulario.username).first()
    
    if not user:

        raise HTTPException(status_code=404, detail="Email invalidos")
    
    elif not bcrypt_context.verify(dadoos_formulario.password, user.senha):

        raise HTTPException(status_code=404, detail=("Senha invalida"))
    
    access_token= criar_token(user.id,)
    refresh_token= criar_token(user.id, data_exp= timedelta(days=7))

    session.refresh(user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh token": refresh_token
    }

@user_router.post("/login-refresh")
async def login_refresh(dados_formulario: OAuth2PasswordRequestForm = Depends(), session=Depends(sessao)):

    user = session.query(Usuario).filter(
        Usuario.email == dados_formulario.username
    ).first()

    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    if not bcrypt_context.verify(
        dados_formulario.password,
        user.senha
    ):
        raise HTTPException(401, "Senha inválida")

    access_token = criar_token(
        user.id
    )

    refresh_token = criar_token(
        user.id,
        data_exp=timedelta(days=7)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@user_router.patch("/usuario/atualizarperfil", status_code=200)
async def editar_perfil(bio:str, foto:str, session= Depends(sessao), user: Usuario = Depends(verificar_token)):
    
    user.bio=bio
    user.foto= foto

    session.commit()
    session.refresh(user)

    return user

@user_router.delete("/usuario/{id_usuario}", status_code=200)
async def removerusuario(id_usuario:int, user: Usuario = Depends(verificar_token),  session=Depends(sessao)):

    u= session.query(Usuario).filter(Usuario.id == id_usuario).first()

    if not u:
        raise HTTPException(status_code=400, detail="usuario não existe")
    
    verificar_excluir(u.id, user, session)

    session.delete(u)
    session.commit()

    return u

@user_router.get("/refresh")
async def use_refresh_token(token):

    refresh_token = criar_token(token, data_exp=timedelta(days=7))

    return {
            "token de acesso": refresh_token,
            "tipo do token": "Bearrer"
           }