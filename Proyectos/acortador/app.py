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
            cursor.execute("SELECT original_url FROM urls WHERE shortened_url = :short_url", {'short_url': original_url})
            row = cursor.fetchone()

            if row:
                original_url = row[0]
                return redirect(original_url, code=302)
            else:
                return jsonify({'error': 'URL acortada no encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)
