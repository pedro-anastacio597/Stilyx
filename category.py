from dependecis import sessao
from models import categoria

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
    ]

    session = next(sessao())

    try:
        for nome in Categorias:
            existe = session.query(categoria).filter(
                categoria.nome == nome
            ).first()

            if not existe:
                session.add(categoria(nome=nome))

        session.commit()

    finally:
        session.close()

