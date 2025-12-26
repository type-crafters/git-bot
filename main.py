from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
from typing import Optional
from bot import DiscordNotificationBot

discord_bot = DiscordNotificationBot()

# Lifespan para manejar el inicio y cierre del bot
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Iniciar el bot de Discord en el background
    bot_task = asyncio.create_task(discord_bot.start())
    
    # Esperar un poco para que el bot se conecte
    await asyncio.sleep(3)
    
    print("🚀 FastAPI iniciado")
    print("📡 Bot de Discord en ejecución")
    
    yield
    
    # Shutdown: Cerrar el bot
    print("🛑 Cerrando bot de Discord...")
    await discord_bot.close()
    bot_task.cancel()

app = FastAPI(
    title="Git Notifications Bot",
    description="Bot de notificaciones para GitHub y GitLab",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Ruta raíz con información del servicio"""
    return {
        "status": "Server is running",
        "version": "1.0.0",
        "bot_status": str(discord_bot.bot.user) if discord_bot.bot.user else "disconnected",
        "endpoints": {
            "github": "/webhook/github",
            "gitlab": "/webhook/gitlab",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    bot_ready = discord_bot.bot.is_ready()
    return {
        "status": "healthy" if bot_ready else "starting",
        "bot_connected": bot_ready,
        "bot_user": str(discord_bot.bot.user) if discord_bot.bot.user else None
    }

@app.post("/webhook/github")
async def github_webhook(
    request: Request,
    x_github_event: Optional[str] = Header(None)
):
    """Endpoint para recibir webhooks de GitHub"""
    try:
        data = await request.json()
        
        if not data:
            print("❌ No se recibieron datos")
            raise HTTPException(status_code=400, detail="No data received")
        
        print(f"✅ Webhook recibido de GitHub")
        print(f"📦 Evento: {x_github_event or 'unknown'}")
        
        # Detectar evento de push (commit)
        if 'commits' in data and data.get('ref'):
            print(f"🔔 Nuevo commit detectado en {data['repository']['full_name']}")
            
            # Formatear y enviar mensaje
            message = discord_bot.format_github_message(data)
            success = await discord_bot.send_notification(message)
            
            if success:
                return {"status": "success", "message": "Notification sent"}
            else:
                raise HTTPException(status_code=404, detail="Discord channel not found")
        
        print(f"⚠️ Evento ignorado (no es un push)")
        return {"status": "ignored", "message": "Not a push event"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook/gitlab")
async def gitlab_webhook(request: Request):
    """Endpoint para recibir webhooks de GitLab"""
    try:
        data = await request.json()
        
        if not data:
            raise HTTPException(status_code=400, detail="No data received")
        
        print(f"✅ Webhook recibido de GitLab")
        
        # Detectar evento de push
        if data.get('object_kind') == 'push':
            print(f"🔔 Nuevo commit detectado en {data['project']['path_with_namespace']}")
            
            # Formatear y enviar mensaje
            message = discord_bot.format_gitlab_message(data)
            success = await discord_bot.send_notification(message)
            
            if success:
                return {"status": "success", "message": "Notification sent"}
            else:
                raise HTTPException(status_code=404, detail="Discord channel not found")
        
        print(f"⚠️ Evento ignorado (no es un push)")
        return {"status": "ignored", "message": "Not a push event"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=5000,
        reload=True,
        log_level="info"
    )