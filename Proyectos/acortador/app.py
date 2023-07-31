import random
import string
import oracledb
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()

# Montar el directorio "static" para servir el archivo index.html
app.mount("/static", StaticFiles(directory="."), name="static")


# Función para generar una cadena acortada aleatoria
def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(8))
    return short_url


# Ruta para acortar una URL larga
@app.post("/shorten/", response_class=HTMLResponse)
async def shorten_url(url: str = Form(...)):
    if not url:
        raise HTTPException(status_code=400, detail="URL no proporcionada")

    # Realizar la conexión a la base de datos de Oracle
    with oracledb.connect("usuario/oracle@nombre_de_servicio") as conn:
        # Crear un cursor para interactuar con la base de datos
        with conn.cursor() as cursor:
            # Verificar si la URL ya ha sido acortada previamente
            cursor.execute("SELECT shortened_url FROM urls WHERE original_url = :original_url", {'original_url': url})
            row = cursor.fetchone()
            if row:
                short_url = row[0]
            else:
                # Generar una URL acortada nueva
                short_url = generate_short_url()
                cursor.execute("INSERT INTO urls (original_url, shortened_url) VALUES (:original_url, :short_url)", {'original_url': url, 'short_url': short_url})
                conn.commit()

    # Devolver el HTML con la URL acortada
    return f'<html><body><h1>URL acortada: <a href="{short_url}" target="_blank">{short_url}</a></h1></body></html>'


# Ruta para redireccionar a la URL original
@app.get("/{short_url}", response_class=HTMLResponse)
async def redirect_to_original(short_url: str):
    # Realizar la conexión a la base de datos de Oracle
    with oracledb.connect("usuario/oracle@nombre_de_servicio") as conn:
        # Crear un cursor para interactuar con la base de datos
        with conn.cursor() as cursor:
            # Buscar la URL original en la base de datos
            cursor.execute("SELECT original_url FROM urls WHERE shortened_url = :short_url", {'short_url': short_url})
            row = cursor.fetchone()
            if row:
                original_url = row[0]
                if not original_url.startswith('http://') and not original_url.startswith('https://'):
                    original_url = 'http://' + original_url  # Asegurarse de que la URL tenga el prefijo http:// o https://
                conn.close()
                return f'<html><body><h1>Redirigiendo a: <a href="{original_url}" target="_blank">{original_url}</a></h1></body></html>'
            else:
                conn.close()
                raise HTTPException(status_code=404, detail="URL acortada no encontrada")