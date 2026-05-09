from fastapi import FastAPI,WebSocket
from fastapi.responses import FileResponse
import uvicorn

app=FastAPI()

active_connections: list[WebSocket] = []

@app.get("/")
def read_index():
    return FileResponse("index.html")


@app.get("/healthcheck")
def health_check():
    return {"message": "OK"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await broadcast(data)
    except:
        pass
    finally:
        active_connections.remove(websocket)

async def broadcast(message: str):
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except:
            pass



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
