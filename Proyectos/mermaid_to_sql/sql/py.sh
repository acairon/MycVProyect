#!/bin/bash

# Paso 1: Instalar Certbot
sudo apt update
sudo apt install certbot python3-certbot-apache -y

# Paso 2: Generar el certificado SSL
sudo certbot certonly --apache --agree-tos --non-interactive --email angelshce@gmail.com -d api.angelcairon.com

# Paso 3: Configurar Apache como proxy inverso
sudo a2enmod ssl
sudo a2enmod proxy
sudo a2enmod proxy_http

# Paso 4: Crear archivo de configuración para el proxy inverso
sudo tee /etc/apache2/sites-available/myapi.conf > /dev/null <<EOF
<VirtualHost *:443>
    ServerName tu_dominio

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/tu_dominio/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/tu_dominio/privkey.pem

    ProxyPass / http://10.0.0.98:8000/
    ProxyPassReverse / http://10.0.0.98:8000/

    ErrorLog ${APACHE_LOG_DIR}/myapi_error.log
    CustomLog ${APACHE_LOG_DIR}/myapi_access.log combined
</VirtualHost>
EOF

# Paso 5: Habilitar el sitio y reiniciar Apache
sudo a2ensite myapi
sudo systemctl restart apache2
