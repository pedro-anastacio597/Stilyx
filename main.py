from fastapi import FastAPI, HTTPException,APIRouter
from category import definir_categorias
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer 

app = FastAPI(title="Stylix0.1")


from user_router import user_router
from post_router import post_router
from past_router import past_router
from complaint_router import complaint_router

app.include_router(user_router)
app.include_router(post_router)
app.include_router(past_router)
app.include_router(complaint_router)


definir_categorias()

#banco de dados

# usuarios = []
# posts = []
# pastas = []
# denuncias = []


# #classes de entrada

# from pydantic import BaseModel

# class PerfilUpdate(BaseModel):
#     bio: str
#     foto: str

# class CurtidaEntrada(BaseModel):
#     usuario_id: str

# class ComentarioEntrada(BaseModel):
#     usuario_id: str
#     texto: str

# class AddPostEntrada(BaseModel):
#     post_id: str

# class LoginEntrada(BaseModel):
#     email: EmailStr
#     senha: str

# class UsuarioEntrada(BaseModel):
#     nome: str
#     email: EmailStr
#     senha: str


# class PostEntrada(BaseModel):
#     usuario_id: str
#     imagem: str
#     titulo: str
#     descricao: str
#     categoria: str
#     tag: list[str]= []


# class PastaEntrada(BaseModel):
#     usuario_id: str
#     nome: str


# class DenunciaEntrada(BaseModel):
#     usuario_id: str
#     alvo_id: str
#     motivo: str


# class Usuario(UsuarioEntrada):
#     id: str = ""
#     bio: str = ""
#     foto: str = ""


# class Post(PostEntrada):
#     id: str = ""
#     data: str = ""
#     curtidas: List[str] = []
#     comentarios: List[str] = []


# class Pasta(PastaEntrada):
#     id: str = ""
#     posts: List[str] = []


# class Denuncia(DenunciaEntrada):
#     id: str = ""
#     data: str = ""


# #usuario

# @app.post("/usuarios", status_code=201)
# def cadastro(dados: UsuarioEntrada):

#     u = Usuario(id=str(uuid.uuid4()), **dados.model_dump())
#     usuarios.append(u)
#     return u



# @app.post("/login", status_code=200)
# def login(dados: LoginEntrada):

#     for u in usuarios:
#         if u.email == dados.email and u.senha == dados.senha:
#             return {"msg": "OK", "id": u.id}

#     raise HTTPException(401, "erro login")


# #post

# @app.post("/posts", status_code=201)
# def criar_post(dados: PostEntrada):

#     p = Post(
#         id=str(uuid.uuid4()),
#         data=str(datetime.now()),
#         curtidas=[],
#         comentarios=[],
#         **dados.model_dump()
#     )

#     posts.append(p)
#     return p


# @app.get("/posts", status_code=200)
# def listar_posts():
#     return posts


# #pasta

# @app.post("/pastas", status_code=201)
# def criar_pasta(dados: PastaEntrada):

#     p = Pasta(
#         id=str(uuid.uuid4()),
#         posts=[],
#         **dados.model_dump()
#     )

#     pastas.append(p)
#     return p


# @app.post("/pastas/{id}/add", status_code=200)
# def adicionar_post(id: str, dados: AddPostEntrada):

#     for p in pastas:
#         if p.id == id:
#             p.posts.append(dados.post_id)
#             return p

#     raise HTTPException(404, "pasta não existe")


# #curtir

# @app.post("/posts/{id}/curtir", status_code=200)
# def curtir(id: str, dados: CurtidaEntrada):

#     for p in posts:
#         if p.id == id:

#             if dados.usuario_id not in p.curtidas:
#                 p.curtidas.append(dados.usuario_id)

#             return p

#     raise HTTPException(404, "post não existe")


# # comentar

# @app.post("/posts/{id}/comentar", status_code=201)
# def comentar(id: str, dados: ComentarioEntrada):

#     if not dados.texto.strip():
#         raise HTTPException(400, "comentário vazio")

#     for p in posts:
#         if p.id == id:
#             p.comentarios.append(f"{dados.usuario_id}: {dados.texto}")
#             return p

#     raise HTTPException(404, "post não existe")


# @app.post("/buscar", status_code=200)
# def buscar(q: str):

#     return [
#         p for p in posts
#         if (
#             q.lower() in p.titulo.lower()
#             or q.lower() in p.categoria.lower()
#             or any(q.lower() in tag.lower() for tag in p.tag)
#         )
#     ]


# #atualizar perfil

# @app.patch("/usuarios/{id}", status_code=200)
# def editar_perfil(id: str, dados: PerfilUpdate):

#     for u in usuarios:
#         if u.id == id:
#             u.bio = dados.bio
#             u.foto = dados.foto
#             return u

#     raise HTTPException(404, "usuario não existe")


# #Denuncia 

# @app.post("/denunciar", status_code=201)
# def denunciar(dados: DenunciaEntrada):

#     d = Denuncia(
#         id=str(uuid.uuid4()),
#         data=str(datetime.now()),
#         **dados.model_dump()
#     )

#     denuncias.append(d)
#     return d


# @app.delete("/posts/{id}", status_code=204)
# def remover_post(id: str):

#     for p in posts:
#         if p.id == id:
#             posts.remove(p)
#             return p

#     raise HTTPException(404, "post não existe")