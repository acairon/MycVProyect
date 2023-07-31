import sqlite3
import random
import string
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS

app = Flask(__name__)


CORS(app)  # Habilitar CORS en la aplicación Flask

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

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()

    # Verificar si la URL ya ha sido acortada previamente
    cursor.execute("SELECT shortened_url FROM urls WHERE original_url=?", (original_url,))
    row = cursor.fetchone()
    if row:
        short_url = row[0]
    else:
        # Generar una URL acortada nueva
        short_url = generate_short_url()
        cursor.execute("INSERT INTO urls (original_url, shortened_url) VALUES (?, ?)", (original_url, short_url))
        conn.commit()

    conn.close()

    return jsonify({'shortened_url': f'http://apishorten.angelcairon.com/{short_url}'}), 200


# Ruta para redireccionar a la URL original
@app.route('/<short_url>')
def redirect_to_original(short_url):
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()

    # Buscar la URL original en la base de datos
    cursor.execute("SELECT original_url FROM urls WHERE shortened_url=?", (short_url,))
    row = cursor.fetchone()

    if row:
        original_url = row[0]
        conn.close()
        return redirect(original_url, code=302)
    else:
        conn.close()
        return jsonify({'error': 'URL acortada no encontrada'}), 404


if __name__ == '__main__':
    # Crear la tabla 'urls' en la base de datos si no existe
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS urls (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        original_url TEXT NOT NULL,
                        shortened_url TEXT NOT NULL UNIQUE
                    )''')
    conn.commit()
    conn.close()