from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import phrases_getter

from mangum import Mangum

app = FastAPI()

handler = Mangum(app)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/frases/{q}")
def get_phrases(q: str, n: int, max_len: int):
    getter = phrases_getter.PhrasesGetter(q, max_len)
    phrases = getter.get_phrases(n)
    return {"query": q, "n": n, "max_len": max_len, "frases": phrases}

@app.get("/random_frase")
def get_random_phrase(q: str, max_len: int):
    getter = phrases_getter.PhrasesGetter(q, max_len)
    phrase = getter.get_random_phrase()
    return {"query": q, "max_len": max_len, "frase": phrase}

@app.get("/random_einstein")
def get_random_einstein():
    return get_random_phrase("einstein", 140)