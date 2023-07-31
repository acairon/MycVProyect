import random
import string
import oracledb
import os
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

CORS(app)  # Habilitar CORS en la aplicación Flask

un = os.environ.get('PYTHON_USERNAME')
pw = os.environ.get('PYTHON_PASSWORD')
cs = os.environ.get('PYTHON_CONNECTSTRING')

# Función para generar una cadena acortada aleatoria
def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(8))
    return short_url

# Ruta para acortar una URL larga
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({'error': 'URL no proporcionada'}), 400

    # Realizar la conexión a la base de datos de Oracle
    with oracledb.connect(user=un, password=pw, dsn=cs) as conn:
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

    return jsonify({'shortened_url': short_url}), 200  # Solo envía el segmento específico del enlace acortado

# Ruta para redireccionar a la URL original
@app.route('/<short_url>')
def redirect_to_original(short_url):
    # Realizar la conexión a la base de datos de Oracle
    with oracledb.connect(user=un, password=pw, dsn=cs) as conn:
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
                return redirect(original_url, code=302)  # Redirigir a la URL original
            else:
                conn.close()
                return jsonify({'error': 'URL acortada no encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)