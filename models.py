from fastapi import FastAPI, HTTPException,APIRouter, Depends
from pydantic import BaseModel, EmailStr

class UsuarioEntrada(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    admin: bool
    foto: str | None = None
    bio: str  | None = None

class PostEntrada(BaseModel):
    imagem: str
    titulo: str
    descricao: str
    categoria: list[str]
    tag: list[str]

class comentario(BaseModel):
    texto: str
    id_post: int

class PastaEntrada(BaseModel):
    nome: str
    descricao: str | None =None
    estado: bool

class DenunciaEntrada(BaseModel):
    id_post: int | None = None
    id_alvo: int 
    motivo: str