from sqlalchemy import (
    create_engine, Column, String, Integer, ForeignKey,
    Date, Boolean
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import date

db = create_engine("sqlite:///banco.db")
Base = declarative_base()



class Usuario(Base):
    __tablename__ = "usuario"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, unique=True, nullable=False)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String, nullable=False)
    admin = Column("admin", Boolean, default=False)
    foto = Column("foto", String)
    bio = Column("bio", String)

    posts = relationship("Post", back_populates="usuario", cascade="all, delete")
    pastas = relationship("Pasta", back_populates="usuario", cascade="all, delete")
    curtidas = relationship("Curtida", back_populates="usuario", cascade="all, delete")
    comentarios = relationship("Comentario", back_populates="usuario", cascade="all, delete")

    denuncias_feitas = relationship(
        "Denuncia",
        foreign_keys="Denuncia.id_usuario",
        back_populates="usuario",
        cascade="all, delete"
    )

    denuncias_recebidas = relationship(
        "Denuncia",
        foreign_keys="Denuncia.id_alvo",
        back_populates="alvo",
        cascade="all, delete"
    )

    def __init__(self, nome, email, senha,admin=False, bio= None, foto=None ):
        self.nome= nome
        self.email= email
        self.admin= admin
        self.senha= senha
        self.bio= bio
        self.foto= foto



class Post(Base):
    __tablename__ = "post"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    imagem = Column("imagem", String, nullable=False)
    titulo = Column("titulo", String, nullable=False)
    descricao = Column("descricao", String, nullable=False)
    id_usuario = Column("id_usuario", Integer, ForeignKey("usuario.id"))
    data_criacao = Column("data_criacao", Date, default=date.today)

    usuario = relationship("Usuario", back_populates="posts")

    comentarios = relationship("Comentario", back_populates="post", cascade="all, delete")
    curtidas = relationship("Curtida", back_populates="post", cascade="all, delete")
    denuncias = relationship("Denuncia", back_populates="post", cascade="all, delete")

    post_pasta = relationship("PastaPost", back_populates="post", cascade="all, delete")
    post_tag = relationship("PostTag", back_populates="post", cascade="all, delete")
    post_categoria = relationship("PostCategoria", back_populates="post", cascade="all, delete")

    def __init__(self, imagem, titulo, descricao, id_usuario):
        self.imagem= imagem
        self.titulo= titulo
        self.descricao= descricao
        self.id_usuario= id_usuario



class Comentario(Base):
    __tablename__ = "comentario"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    texto = Column("texto", String, nullable=False)
    id_usuario = Column("id_usuario", Integer, ForeignKey("usuario.id"))
    id_post = Column("id_post", Integer, ForeignKey("post.id"))

    usuario = relationship("Usuario", back_populates="comentarios")
    post = relationship("Post", back_populates="comentarios")

    def __init__(self, texto, id_usuario, id_post):
        self.texto= texto
        self.id_usuario= id_usuario
        self.id_post= id_post


class Curtida(Base):
    __tablename__ = "curtida"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_post = Column("id_post", Integer, ForeignKey("post.id"))
    id_usuario = Column("id_usuario", Integer, ForeignKey("usuario.id"))

    usuario = relationship("Usuario", back_populates="curtidas")
    post = relationship("Post", back_populates="curtidas")

    def __init__(self, id_post, id_usuario ):
        self.id_post= id_post
        self.id_usuario= id_usuario


class Pasta(Base):
    __tablename__ = "pasta"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    descricao = Column("descricao", String)
    estado = Column("estado", Boolean, nullable=False)
    id_usuario = Column("id_usuario", Integer, ForeignKey("usuario.id"))

    usuario = relationship("Usuario", back_populates="pastas")
    pasta_post = relationship("PastaPost", back_populates="pasta", cascade="all, delete")

    def __init__(self, nome, descricao, id_usuario, estado= False):
        self.nome= nome
        self.descricao= descricao
        self.estado= estado
        self.id_usuario= id_usuario


class Denuncia(Base):
    __tablename__ = "denuncia"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario",Integer, ForeignKey("usuario.id"))
    id_post = Column("id_post",Integer, ForeignKey("post.id"))
    id_alvo = Column("id_alvo",Integer, ForeignKey("usuario.id"))
    motivo = Column("motivo", String, nullable=False)
    data_criacao = Column(Date, default=date.today)

    usuario = relationship(
        "Usuario",
        foreign_keys=[id_usuario],
        back_populates="denuncias_feitas"
    )

    alvo = relationship(
        "Usuario",
        foreign_keys=[id_alvo],
        back_populates="denuncias_recebidas"
    )

    post = relationship("Post", back_populates="denuncias")

    def __init__(self, id_usuario, id_post, id_alvo, motivo):
        self.id_usuario= id_usuario
        self.id_alvo=id_alvo
        self.id_post= id_post
        self.motivo= motivo



class Tag(Base):
    __tablename__ = "tag"

    id = Column("id",Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)

    post_tag = relationship("PostTag", back_populates="tag", cascade="all, delete")

    def __init__(self,nome):
        self.nome= nome



class Categoria(Base):
    __tablename__ = "categoria"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, unique=True, nullable=False)

    post_categoria = relationship("PostCategoria", back_populates="categoria", cascade="all, delete")

    def __init__(self,nome):
        self.nome= nome


class PastaPost(Base):
    __tablename__ = "pasta_post"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_post = Column("id_post",Integer, ForeignKey("post.id"))
    id_pasta = Column("id_pasta", Integer, ForeignKey("pasta.id"))

    post = relationship("Post", back_populates="post_pasta")
    pasta = relationship("Pasta", back_populates="pasta_post")

    def __init__(self,id_post, id_pasta):
        self.id_post= id_post
        self.id_pasta= id_pasta


class PostCategoria(Base):
    __tablename__ = "post_categoria"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_post = Column("id_post", Integer, ForeignKey("post.id"))
    id_categoria = Column("id_categoria", Integer, ForeignKey("categoria.id"))

    post = relationship("Post", back_populates="post_categoria")
    categoria = relationship("Categoria", back_populates="post_categoria")

    def __init__(self,id_post, id_categoria):
        self.id_post= id_post
        self.id_categoria= id_categoria


class PostTag(Base):
    __tablename__ = "post_tag"

    id = Column("id" ,Integer, primary_key=True, autoincrement=True)
    id_post = Column("id_post" ,Integer, ForeignKey("post.id"))
    id_tag = Column("id_tag" ,Integer, ForeignKey("tag.id"))

    post = relationship("Post", back_populates="post_tag")
    tag = relationship("Tag", back_populates="post_tag")

    def __init__(self,id_post, id_tag):
        self.id_post= id_post
        self.id_tag= id_tag