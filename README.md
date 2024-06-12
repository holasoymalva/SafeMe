# SafeMe - Verificación de Mensajes y Sitios Bancarios

Esta es una API RESTful para verificar la legitimidad de mensajes y sitios web bancarios, creada con Flask.

## Tabla de Contenidos

- [Instalación](#instalación)
- [Uso](#uso)
- [Rutas de la API](#rutas-de-la-api)
- [Ejemplos de uso](#ejemplos-de-uso)
- [Contribución](#contribución)
- [Licencia](#licencia)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/holasoymalva/SafeMe.git
   cd SafeMe
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta la aplicación Flask:
   ```bash
   python app.py
   ```

2. La API estará disponible en `http://127.0.0.1:5000`.

## Rutas de la API

### Verificar Mensaje

- **URL**: `/verificar_mensaje`
- **Método**: `POST`
- **Descripción**: Verifica si un mensaje es sospechoso.
- **Cuerpo de la solicitud**:
  ```json
  {
    "mensaje": "Contenido del mensaje",
    "remitente": "correo@dominio.com"
  }
  ```

### Verificar Sitio Bancario

- **URL**: `/verificar_sitio_bancario`
- **Método**: `POST`
- **Descripción**: Verifica si un sitio web bancario es legítimo.
- **Cuerpo de la solicitud**:
  ```json
  {
    "url": "https://example.com"
  }
  ```

## Ejemplos de uso

### Usando `curl`

- **Verificar mensaje**:
  ```bash
  curl -X POST http://127.0.0.1:5000/verificar_mensaje -H "Content-Type: application/json" -d '{"mensaje": "Urgente: Verifique su cuenta bancaria", "remitente": "fraude@example.com"}'
  ```

- **Verificar sitio bancario**:
  ```bash
  curl -X POST http://127.0.0.1:5000/verificar_sitio_bancario -H "Content-Type: application/json" -d '{"url": "https://example.com"}'
  ```

### Usando Postman

1. Abre Postman y crea una nueva solicitud.
2. Selecciona el método HTTP adecuado (POST).
3. Introduce la URL de la API (`http://127.0.0.1:5000/verificar_mensaje` o `http://127.0.0.1:5000/verificar_sitio_bancario`).
4. Selecciona el tipo de cuerpo como JSON y proporciona los datos en el formato requerido.
5. Haz clic en "Send" y revisa la respuesta.

## Contribución

¡Las contribuciones son bienvenidas! Por favor, sigue estos pasos para contribuir:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios necesarios y haz commit (`git commit -m 'Agrega nueva funcionalidad'`).
4. Empuja los cambios a tu repositorio fork (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request para revisar y fusionar los cambios.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para obtener más información.
