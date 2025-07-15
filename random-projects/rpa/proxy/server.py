from fastapi import FastAPI, Response
import httpx

app = FastAPI()

@app.get("/proxy")
async def proxy_file(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        content_type = "application/pdf"  # Force correct MIME type
        return Response(content=response.content, media_type=content_type)