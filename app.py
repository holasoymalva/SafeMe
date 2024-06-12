import json
import os
import re
import requests
import tldextract
from datetime import datetime, timedelta

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

# Función para cargar los datos de los medicamentos desde el archivo JSON
def load_medicamentos():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    else:
        return []

# Función para guardar los datos de los medicamentos en el archivo JSON
def save_medicamentos(medicamentos):
    with open(FILE_PATH, 'w') as file:
        json.dump(medicamentos, file, indent=2)

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
        print("El sitio web no tiene un certificado SSL válido.")
        return False

    dominio = analizar_url(url)
    if dominio in dominios_bancarios_oficiales:
        print(f"El sitio web {url} es oficial.")
        return True
    else:
        print(f"El dominio {dominio} no está en la lista de dominios bancarios oficiales.")
        return False

def verificar_mensaje(mensaje, remitente):
    # Verificar si el mensaje contiene palabras clave de fraude
    for palabra in palabras_clave_fraude:
        if re.search(r'\b' + palabra + r'\b', mensaje, re.IGNORECASE):
            print(f"Advertencia: El mensaje contiene la palabra clave sospechosa '{palabra}'.")

    # Verificar si el remitente tiene un dominio oficial
    dominio = remitente.split('@')[-1]
    if dominio not in dominios_oficiales:
        print(f"Advertencia: El remitente '{remitente}' no pertenece a un dominio oficial.")
    else:
        print(f"El remitente '{remitente}' pertenece a un dominio oficial.")

    # Verificar si hay enlaces sospechosos en el mensaje
    enlaces = re.findall(r'http[s]?://\S+', mensaje)
    for enlace in enlaces:
        if not any(dominio in enlace for dominio in dominios_oficiales):
            print(f"Advertencia: El mensaje contiene un enlace sospechoso: {enlace}")
        else:
            print(f"El enlace '{enlace}' parece legítimo.")

# Ejemplo de uso
if __name__ == '__main__':
    while True:
        print("\n1. Verificar mensaje")
        print("2. Verificar sitio bancario")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            mensaje = input("Ingrese el mensaje recibido: ")
            remitente = input("Ingrese el correo electrónico del remitente: ")
            verificar_mensaje(mensaje, remitente)
        elif opcion == '2':
            url = input("Ingrese la URL del sitio web para verificar: ")
            if es_sitio_bancario_legitimo(url):
                print("El sitio web es oficial.")
            else:
                print("El sitio web puede ser una estafa.")
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Intente nuevamente.")
