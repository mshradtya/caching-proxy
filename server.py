from fastapi import FastAPI, Request
from fastapi.responses import Response
import httpx
import uvicorn
from typing import Dict, Tuple

cache: Dict[str, Tuple[bytes, int, Dict[str, str]]] = {}

def start_server(port: int, origin: str):
    print(f"Starting server on port {port}")
    print(f"Proxying to origin: {origin}")

    app = FastAPI()

    def get_url_string(path: str, query: str):
        if path and query:
            return f"{origin}/{path}?{query}"
        elif not path and query:
            return f"{origin}?{query}"
        elif path and not query:
            return f"{origin}/{path}"
        else:
            return origin

    @app.get("/{path:path}")
    async def proxy(path: str, request: Request): # type: ignore
        query = request.url.query
        url = get_url_string(path, query)

        # check cache
        if url in cache:
            print(f"[CACHE] HIT: {url}")
            content, status_code, headers = cache[url]
            headers["X-Cache"] = "HIT"
            return Response(content=content, status_code=status_code, headers=headers)

        async with httpx.AsyncClient() as client:
            response = await client.get(url)

        # remove headers that can mess with proxy behavior
        excluded_headers = ["content-length", "transfer-encoding", "content-encoding", "connection"]
        headers = {
            k: v for k, v in response.headers.items()
            if k.lower() not in excluded_headers
        }
        headers["X-Cache"] = "MISS"

        # cache the response
        cache[url] = (response.content, response.status_code, headers.copy())

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=headers
        )

    uvicorn.run(app, host="0.0.0.0", port=port)
