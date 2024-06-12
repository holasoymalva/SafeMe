import json
import os
import re
import requests
import tldextract
from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista de palabras clave comunes en fraudes
palabras_clave_fraude = [
    'urgente', 'inmediato', 'verifique', 'alerta', 'reembolso', 'no reconocido', 'suspendido', 
    'congelado', 'aclaración', 'iniciar sesión', 'contraseña', 'detalles bancarios', 'verificación'
]

# Lista de dominios de correo electrónico oficiales conocidos
dominios_oficiales = [
    'bankofamerica.com', 'chase.com', 'wellsfargo.com', 'citibank.com', 'hsbc.com',
    # Añade más dominios según sea necesario
]

# Lista de dominios bancarios oficiales conocidos
dominios_bancarios_oficiales = [
    'bankofamerica.com', 'chase.com', 'wellsfargo.com', 'citibank.com', 'hsbc.com',
    # Añade más dominios según sea necesario
]

def verificar_certificado_ssl(url):
    try:
        response = requests.get(url, timeout=10)
        return response.url.startswith('https://')
    except requests.exceptions.SSLError:
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error al verificar el certificado SSL: {e}")
        return False

def analizar_url(url):
    ext = tldextract.extract(url)
    dominio = f"{ext.domain}.{ext.suffix}"
    return dominio

def es_sitio_bancario_legitimo(url):
    if not verificar_certificado_ssl(url):
        return {"status": "error", "message": "El sitio web no tiene un certificado SSL válido."}

    dominio = analizar_url(url)
    if dominio in dominios_bancarios_oficiales:
        return {"status": "success", "message": f"El sitio web {url} es oficial."}
    else:
        return {"status": "error", "message": f"El dominio {dominio} no está en la lista de dominios bancarios oficiales."}

def verificar_mensaje(mensaje, remitente):
    resultados = []
    # Verificar si el mensaje contiene palabras clave de fraude
    for palabra in palabras_clave_fraude:
        if re.search(r'\b' + palabra + r'\b', mensaje, re.IGNORECASE):
            resultados.append(f"Advertencia: El mensaje contiene la palabra clave sospechosa '{palabra}'.")

    # Verificar si el remitente tiene un dominio oficial
    dominio = remitente.split('@')[-1]
    if dominio not in dominios_oficiales:
        resultados.append(f"Advertencia: El remitente '{remitente}' no pertenece a un dominio oficial.")
    else:
        resultados.append(f"El remitente '{remitente}' pertenece a un dominio oficial.")

    # Verificar si hay enlaces sospechosos en el mensaje
    enlaces = re.findall(r'http[s]?://\S+', mensaje)
    for enlace in enlaces:
        if not any(dominio in enlace for dominio in dominios_oficiales):
            resultados.append(f"Advertencia: El mensaje contiene un enlace sospechoso: {enlace}")
        else:
            resultados.append(f"El enlace '{enlace}' parece legítimo.")

    return resultados

@app.route('/verificar_mensaje', methods=['POST'])
def api_verificar_mensaje():
    data = request.json
    mensaje = data.get('mensaje')
    remitente = data.get('remitente')
    if not mensaje or not remitente:
        return jsonify({"status": "error", "message": "Debe proporcionar el mensaje y el remitente."}), 400

    resultados = verificar_mensaje(mensaje, remitente)
    return jsonify({"status": "success", "resultados": resultados})

@app.route('/verificar_sitio_bancario', methods=['POST'])
def api_verificar_sitio_bancario():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"status": "error", "message": "Debe proporcionar la URL."}), 400

    resultado = es_sitio_bancario_legitimo(url)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
