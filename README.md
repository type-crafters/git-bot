# Git Notifications Bot - FastAPI Edition

Bot de notificaciones de Discord para recibir eventos de GitHub y GitLab mediante webhooks.

## 🏗️ Arquitectura

El proyecto está desacoplado en dos componentes principales:

- **`bot.py`**: Maneja toda la lógica del bot de Discord
- **`main.py`**: API REST con FastAPI que recibe webhooks

## 📋 Requisitos

- Python 3.8+
- Discord Bot Token
- ID del canal de Discord

## 🚀 Instalación

1. **Clonar el repositorio e instalar dependencias:**

```bash
pip install -r requirements.txt
```

2. **Configurar variables de entorno:**

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

```env
DISCORD_BOT_TOKEN=tu_token_aqui
DISCORD_CHANNEL_ID=123456789
```

3. **Ejecutar el servidor:**

```bash
python main.py
```

O con uvicorn directamente:

```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

## 📡 Endpoints

### `GET /`
Información general del servicio

### `GET /health`
Health check del servicio y estado del bot

### `POST /webhook/github`
Recibe webhooks de GitHub para eventos de push

### `POST /webhook/gitlab`
Recibe webhooks de GitLab para eventos de push

### `GET /docs`
Documentación interactiva de Swagger UI (automática con FastAPI)

## 🔧 Configuración de Webhooks

### GitHub

1. Ve a tu repositorio → Settings → Webhooks → Add webhook
2. Payload URL: `http://tu-servidor:5000/webhook/github`
3. Content type: `application/json`
4. Selecciona eventos: **Push events**

### GitLab

1. Ve a tu repositorio → Settings → Webhooks
2. URL: `http://tu-servidor:5000/webhook/gitlab`
3. Marca el evento: **Push events**

## 🧪 Testing

Puedes probar los endpoints con curl:

```bash
# Health check
curl http://localhost:5000/health

# Información del servicio
curl http://localhost:5000/
```

## 📦 Estructura del Proyecto

```
.
├── bot.py              # Lógica del bot de Discord
├── main.py             # API FastAPI
├── requirements.txt    # Dependencias
├── .env.example        # Ejemplo de variables de entorno
└── README.md          # Documentación
```

## 🎯 Ventajas de esta Arquitectura

- **Desacoplamiento**: El bot y la API son independientes
- **Escalabilidad**: Fácil de escalar horizontalmente
- **Mantenibilidad**: Código organizado y fácil de mantener
- **Testing**: Cada componente se puede testear por separado
- **Documentación automática**: FastAPI genera Swagger UI
- **Type hints**: Mejor IDE support y detección de errores
- **Async/Await nativo**: Mejor performance

## 🔒 Producción

Para producción, considera:

1. Usar un servidor ASGI como Gunicorn con workers de Uvicorn
2. Configurar HTTPS con certificados SSL
3. Implementar rate limiting
4. Añadir autenticación en los webhooks
5. Usar variables de entorno seguras (secrets manager)

Ejemplo con Gunicorn:

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000
```