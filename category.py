from dependecis import sessao
from database import Categoria

def definir_categorias():

    Categorias = [
        "Unhas decoradas",
        "Receitas",
        "Comida saudavel",
        "Cores",
        "Tecnologia",
        "Moda",
        "Natureza",
        "Saúde",
        "Decoração",
        "Faça Você Mesmo (DIY)",
        "Beleza",
        "Viagens",
        "Animais",
        "Automóveis",
        "Celebridade",
        "Ciência",
        "Esporte",
    ]

    session = next(sessao())

    try:
        for nome in Categorias:
            existe = session.query(Categoria).filter(
                Categoria.nome == nome
            ).first()

            if not existe:
                session.add(Categoria(nome=nome))

        session.commit()

    finally:
        session.close()

