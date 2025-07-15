from fastapi import FastAPI, Response
import httpx

app = FastAPI()

@app.get("/proxy")
async def proxy_file(server: str, file_id: str, filename: str):
    """
    Proxy a file from GoFile.io.
    """
    async with httpx.AsyncClient() as client:
        url = f"https://{server}.gofile.io/download/{file_id}/{filename}"
        print(f"Fetching URL: {url}")
        response = await client.get(url)
        content_type = "application/pdf"  # Force correct MIME type
        return Response(content=response.content, media_type=content_type)