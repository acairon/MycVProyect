import random
import string
import oracledb
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

# Conexión a la base de datos de Oracle
def get_db_connection():
    conn = oracledb.connect('usuario/oracle@nombre_de_servicio')
    return conn

# Función para generar una cadena acortada aleatoria
def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(8))
    return short_url

# Modelo para la solicitud de acortar URL
class ShortenRequest(BaseModel):
    url: str

# Modelo para la respuesta de URL acortada
class ShortenResponse(BaseModel):
    shortened_url: str

# Ruta para acortar una URL larga
@app.post("/shorten", response_model=ShortenResponse)
def shorten_url(request: ShortenRequest):
    original_url = request.url

    # Realizar la conexión a la base de datos de Oracle
    with get_db_connection() as conn:
        # Crear un cursor para interactuar con la base de datos
        with conn.cursor() as cursor:
            # Verificar si la URL ya ha sido acortada previamente
            cursor.execute("SELECT shortened_url FROM urls WHERE original_url = :original_url", {'original_url': original_url})
            row = cursor.fetchone()
            if row:
                short_url = row[0]
            else:
                # Generar una URL acortada nueva
                short_url = generate_short_url()
                cursor.execute("INSERT INTO urls (original_url, shortened_url) VALUES (:original_url, :short_url)", {'original_url': original_url, 'short_url': short_url})
                conn.commit()

    return ShortenResponse(shortened_url=f'http://apishorten.angelcairon.com/{short_url}')

# Ruta para redireccionar a la URL original
@app.get("/{short_url}")
def redirect_to_original(short_url: str, request: Request):
    # Realizar la conexión a la base de datos de Oracle
    with get_db_connection() as conn:
        # Crear un cursor para interactuar con la base de datos
        with conn.cursor() as cursor:
            # Buscar la URL original en la base de datos
            cursor.execute("SELECT original_url FROM urls WHERE shortened_url = :short_url", {'short_url': short_url})
            row = cursor.fetchone()
            if row:
                original_url = row[0]
                return request.redirect(original_url)
            else:
                return "URL acortada no encontrada"
