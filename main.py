from fastapi import FastAPI, APIRouter
from category import definir_categorias


app = FastAPI(title="Stylix0.3")


from user_router import user_router
from post_router import post_router
from past_router import past_router
from complaint_router import complaint_router

app.include_router(user_router)
app.include_router(post_router)
app.include_router(past_router)
app.include_router(complaint_router)


definir_categorias()

