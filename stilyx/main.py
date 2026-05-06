from fastapi import FastAPI, HTTPException,UploadFile,File
from pydantic import BaseModel,Field,HttpUrl,EmailStr
from fastapi.staticfiles import StaticFiles
from typing import List
import uuid
from datetime import datetime,date,timezone
import shutil
import os

app= FastAPI(title="Stilyx", version="0.1")

class usuarioentrada(BaseModel):
    Nome: str
    Emai: EmailStr
    Senha: str
    DataNascimento: date
    Genero: str
    Categorias: List[str]=[]

class usuario(usuarioentrada):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class criarimagem(BaseModel):
    titulo: str
    legenda: str

class imagem(criarimagem):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    autor: str
    datacriacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    url: HttpUrl
    Curtidas=List[str]=[]

class Pastaentrada(BaseModel):
    nome: str
    descricao: str
    estado: str
    imagens: List[str]=[]

class pasta(Pastaentrada):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    idUsuario: str
    
imagens_db=[]
pasta_db=[]
Usuario_bd=[]


@app.post("/usuario", response_model=usuario, status_code=201)
def criarUsuaruio(dados: usuarioentrada):
    u= usuario(**dados.model_dump())
    Usuario_bd.append(u)
    return u

@app.post("/postagem",response_model=imagem, status_code=201)
def publicar(titulo:str,legenda: str, img: UploadFile = File(...)):
    tipo = os.path.splitext(img.filename)[1]
    link = f"{uuid.uuid4()}{tipo}"
    with open(link, "wb") as local:
        local.write(img.file.read())
    Url = f"http://localhost:8000/imagens/{link}"
    novo = imagem(titulo,legenda,url=Url,autor="123")
    imagens_db.append(novo)
    return novo

app.post("/Postagem", response_model=imagem, status_code=201)
def Curtir(IdUsuario=str):
    imagem.Curtidas.append(IdUsuario)

@app.post("/Pasta", response_model=pasta, status_code=201)
def Pastaentrada(dados: Pastaentrada):
    p= pasta(**dados)
    pasta_db.append(p)
    return p
@app.get("/Pasta", response_model=pasta, status_code=200)
def listarPasta(idUsuario):
    lista=[type]
    for p in pasta_db:
        if p.idUsuario ==idUsuario:
            lista.append(p)
        else:
            continue
    return lista
