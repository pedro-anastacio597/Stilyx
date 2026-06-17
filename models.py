from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Date, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import date

db= create_engine("sqlite:///banco.db")

Base = declarative_base()

class usuario(Base):
    __tablename__ = "usuario"

    id= Column("id", Integer, primary_key=True, autoincrement=True)
    nome= Column("nome", String, unique=True, nullable=False)
    email=Column("email", String, nullable=False)
    senha= Column("senha", String, nullable=False)
    foto=Column("foto", String)
    bio= Column("bio", String)

    def __init__(self,nome,email,senha,foto=None ,bio=None):
        self.nome=nome
        self.email=email
        self.senha=senha
        self.foto=foto
        self.bio= bio

    posts = relationship(
        "post",
        back_populates="usuario"
    )


class post(Base):
    __tablename__ = "post"

    id= Column("id", Integer, primary_key=True, autoincrement=True)
    imagem= Column("imagem", String, nullable=False)
    titulo= Column("titulo", String, nullable=False)
    descricao= Column("descricao", String, nullable=False)
    usuario_id= Column("usuario_id", Integer, ForeignKey("usuario.id"))
    data_criacao= Column("data_criacao", Date, default=date.today)

    tags = relationship(
        "tag",
        secondary="post_tag",
        back_populates="posts"
    )

    comentarios = relationship(
        "comentario",
        back_populates="post"
    )

    categorias = relationship(
        "categoria",
        secondary="post_categoria",
        back_populates="posts"
    )

    usuario = relationship(
        "usuario",
        back_populates="posts"
    )

    def __init__(self,imagem,titulo,descricao,id_usuario):
        self.imagem= imagem
        self.titulo= titulo
        self.descricao= descricao
        self.usuario_id= id_usuario
        

class tag(Base):
    __tablename__ = "tag"

    id= Column("id", Integer, primary_key=True, autoincrement=True)
    nome= Column("nome", String, nullable=False)

    posts = relationship(
        "post",
        secondary="post_tag",
        back_populates="tags"
    )

    def __init__(self,nome):
        self.nome= nome


class comentario(Base):
    __tablename__ = "comentario"

    id= Column("id", Integer, primary_key=True, autoincrement=True)
    texto= Column("texto", String, nullable=False)
    id_usuario= Column("id_usuario", Integer, ForeignKey("usuario.id"))
    id_post= Column("id_post", Integer, ForeignKey("post.id"))

    post = relationship(
        "post",
        back_populates="comentarios"
    )

    def __init__(self,texto, id_usuario, id_post):
        self.texto= texto
        self.id_usuario= id_usuario
        self.id_post= id_post

class categoria(Base):
    __tablename__ = "categoria"

    id= Column("id", Integer, primary_key=True, autoincrement=True)
    nome= Column("nome", String,unique=True, nullable=False)

    posts = relationship(
        "post",
        secondary="post_categoria",
        back_populates="categorias"
    )

    def __init__(self,nome):
        self.nome= nome

class curtida(Base):
    __tablename__ = "curtida"

    id= Column("id", Integer, primary_key=True, autoincrement=True)
    id_post= Column("id_post", Integer, ForeignKey("post.id"))
    id_usuario= Column("id_usuario", Integer, ForeignKey("usuario.id"))

    def __init__(self, id_post, id_usuario):
        self.id_post= id_post
        self.id_usuario= id_usuario


class pasta(Base):
    __tablename__ = "pasta"

    id= Column("id", Integer, primary_key=True, autoincrement=True)
    nome= Column("nome", String, nullable=False)
    descricao= Column("descricao", String)
    id_usuario= Column("id_usuario", Integer, ForeignKey("usuario.id"))
    estado= Column("Estado", String, nullable=False)

    def __init__(self,nome,descricao, id_usuario, estado):
        self.nome= nome
        self.descricao= descricao
        self.id_usuario= id_usuario
        self.estado= estado

class pasta_post(Base):
    __tablename__ = "pasta_post"

    id= Column("id", Integer, primary_key=True, autoincrement=True)
    id_post= Column("id_post", Integer, ForeignKey("post.id"))
    id_pasta= Column("id_pasta", Integer, ForeignKey("pasta.id"))

    def __init__(self, id_post, id_pasta):
        self.id_post= id_post
        self.id_pasta= id_pasta


class denuncia(Base):
    __tablename__ = "denuncia"

    id= Column("id", Integer, primary_key=True, autoincrement=True)
    id_usuario= Column("id_usuario", Integer, ForeignKey("usuario.id"))
    id_alvo= Column("id_alvo", Integer, ForeignKey("usuario.id"))
    motivo= Column("motivo", String, nullable=False)
    data_criacao= Column("data_criacao", Date, default=date.today)

    def __init__(self, id_usuario, id_alvo, motivo):
        self.id_usuario= id_usuario
        self.id_alvo= id_alvo
        self.motivo= motivo

   
        
post_categoria = Table(
    "post_categoria",
    Base.metadata,
    Column("id_post", Integer, ForeignKey("post.id")),
    Column("id_categoria", Integer, ForeignKey("categoria.id"))
)

post_tag = Table(
    "post_tag",
    Base.metadata,
    Column("id_post", Integer, ForeignKey("post.id")),
    Column("id_tag", Integer, ForeignKey("tag.id"))
)


