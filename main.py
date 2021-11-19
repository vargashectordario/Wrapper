from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.encoders import jsonable_encoder
from requests.auth import HTTPBasicAuth

import pandas as pd
import requests
import json

class Item(BaseModel):
    identificador:str
    empresa:str
    registroIndex: str
    barrio:str
    ciudad:str
    direccion:str

app = FastAPI()

# variables lupap
key = "b011644b562a93c21a83e1b0398eaa86b358e781"
secret = "2f3625ae38e1557f5ba771ceb2b79d116c05482d"
headers = {'Content-type': 'application/json', 'Accept': '*/*'}
url = "https://batch.api.lupap.co/geocode/v2"

@app.post("/clientes/")
def getItems(items : List[Item]):
    request = jsonable_encoder(items)
    df = pd.DataFrame(request)
    df['country']='co'
    order = df[['identificador','country','ciudad','direccion']]
    order.columns = ['id', 'country', 'city', 'address']
    ciclos = int((len(request)/20)+1)
    inicio = 0
    fin = 20
    i=0
    lista = []
    while i < ciclos:
        paquete = order.iloc[inicio:fin,]
        envio =  paquete.to_json(orient='records')
        envio = json.loads(envio)
        inicio += 20
        fin += 20
        i += 1
        r = requests.post(url, data=json.dumps(envio),headers=headers ,auth=HTTPBasicAuth(key,secret))
        dct = json.loads(r.text)
        lista.append(dct)
    
    respuesta = jsonable_encoder(lista)
    return respuesta
    
    
  


