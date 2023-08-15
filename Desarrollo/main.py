import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    pregunta: str
    autor: str
    respuesta: int
    vistas: int

# py -m uvicorn main:app --reload

app = FastAPI()


@app.get("/leer_elementos/")
async def leer_elementos():
    conn = sqlite3.connect("mathStack.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data")
    resultados = cursor.fetchall()
    conn.close()
    if resultados:
        return [{"ID":resultado[0],"Pregunta": resultado[1], "Autor": resultado[2], "Respuestas": resultado[3],"Vistas":resultado[4]} for resultado in resultados]
    else:
        return {"mensaje": "No hay datos en la base de datos"}


@app.get("/leer_respuestas/{respuestas}/")
async def leer_elemento(respuestas: int):
    conn = sqlite3.connect("mathStack.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data WHERE Respuestas=?", (respuestas,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado is not None:
        return {"ID":resultado[0],"Pregunta": resultado[1], "Autor": resultado[2], "Respuestas": resultado[3],"Vistas":resultado[4]}
    else:
        return {"mensaje": "Datos no encontrados"}

@app.get("/leer_vistas/{vistas}/")
async def leer_elemento(vistas: int):
    conn = sqlite3.connect("mathStack.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data WHERE Vistas=?", (vistas,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado is not None:
        return {"ID":resultado[0],"Pregunta": resultado[1], "Autor": resultado[2], "Respuestas": resultado[3],"Vistas":resultado[4]}
    else:
        return {"mensaje": "Datos no encontrados"}


@app.delete("/eliminar_elemento/{id}/")
async def eliminar_elemento(id: int):
    conn = sqlite3.connect("mathStack.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM data WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return {"mensaje": "Datos eliminados exitosamente"}
