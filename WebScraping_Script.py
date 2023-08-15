import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


def procesar_pagina(soup):

    data=[]

    preguntas=[]
    autores = []
    arrs = []
    respuestas = []
    vistas=[]

    preguntas_sitio = soup.find_all('a',class_="s-link")

    for sitio in preguntas_sitio:
        pregunta = sitio.text.strip()
        preguntas.append(pregunta)

    preguntas.pop(0)
    preguntas.pop(-1)


    autores_sitio=soup.find_all('a', class_='flex--item')

    for sitio in autores_sitio:
        autor=sitio.text.strip()
        autores.append(autor)


    arr_sitio=soup.find_all('div', class_='s-post-summary--stats-item')

    for sitio in arr_sitio:
        arr = sitio.get('title')
        arrs.append(arr)

    for i in arrs:
        palabra= i.split()
        palabra_inicial=palabra[0]
        palabra_final=palabra[-1]
        if palabra_final == "answers":
            respuestas.append(palabra_inicial[0])
        elif palabra_final == "views":
            vistas.append(palabra_inicial[0])

    min_length = min(len(preguntas), len(autores), len(respuestas), len(vistas))

    for i in range( min_length ):
        data.append({
            'Preguntas':preguntas[i],
            'Autores':autores[i],
            'Respuestas':respuestas[i],
            'Vistas':vistas[i]
        })

    df = pd.DataFrame(data)
    fecha_actual = datetime.now().date()
    df.to_csv(f"C:\\Users\\carlo\\OneDrive\\Escritorio\\WebScraping_Maths.StackExchange\\Datos\\Datos_{fecha_actual}", index=False, mode='a')



def obtener_contenido(url):
    response = requests.get(url)
    return response.content



def analizar_contenido(html):
    return BeautifulSoup(html, 'html.parser')



def manejar_paginacion(url_base, num_paginas):
    for i in range(1,num_paginas+1):
        url=url_base + str(i)
        contenido_pagina=obtener_contenido(url)
        soup= analizar_contenido(contenido_pagina)
        procesar_pagina(soup)



url_base="https://math.stackexchange.com/questions?tab=newest&page="

num_paginas=3

manejar_paginacion(url_base,num_paginas)
