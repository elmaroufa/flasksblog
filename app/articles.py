#$commande terminal

#pip install -U Flask==2.0.0

from app import app
import asyncio

@app.get("/data")
async def get_data():
    await asyncio.sleep(1)
    return 'Hello'
