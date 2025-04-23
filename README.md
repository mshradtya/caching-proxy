# Caching Proxy Server

A simple FastAPI-based HTTP proxy server that forwards requests to an origin server and caches responses in memory.

📍 **Project Source:**  
[roadmap.sh → Caching Proxy Server](https://roadmap.sh/projects/caching-server)

## Features

- CLI interface with Typer
- Forwards GET requests to the specified origin
- Caches responses to reduce repeated calls
- Adds `X-Cache: HIT` or `MISS` headers
- Built with FastAPI and httpx

## Usage

### Start the server

```bash
python app.py <port> <origin>
```
