from flask import Flask, request, render_template
import hashlib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    short_url = hashlib.md5(long_url.encode()).hexdigest()[:8]
    return render_template('index.html', short_url=short_url)

if __name__ == '__main__':
    app.run(debug=True)