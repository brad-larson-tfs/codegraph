"""FastAPI server that proxies between browser WebSocket and OpenAI Realtime WS."""

import asyncio
import base64
import json
import os
import secrets
from pathlib import Path
from typing import Dict, List

import openai  # type: ignore
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles # Added for FastAPI

import argparse
import yaml
import uvicorn # Added for FastAPI

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt‑4o‑min")

openai.api_key = OPENAI_API_KEY
openai.base_url = OPENAI_BASE_URL  # azure users: set full endpoint

app = FastAPI(title="ai_chat_gpt41")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Mount static files
static_path = Path(__file__).parent / "static"
templates_path = Path(__file__).parent / "templates"
app.mount("/static", StaticFiles(directory=static_path, html=True), name="static")

# In‑memory conversation store → in production replace with database / Redis
conversations: Dict[str, List[Dict]] = {}

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the single‑page voice chat UI."""
    return FileResponse(Path(__file__).parent / "templates" / "index.html")

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(ws: WebSocket, session_id: str):
    await ws.accept()
    conversations.setdefault(session_id, [])

    # Create connection to OpenAI Realtime API using its WS URL
    realtime_url = f"{OPENAI_BASE_URL}/audio/ws?model={OPENAI_MODEL}"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

    async with openai.AsyncOpenAI().realtime.connect(url=realtime_url, headers=headers) as client_ws:
        async def forward_browser_to_openai():
            try:
                async for msg in ws.iter_bytes():
                    # Expect browser sends raw 16‑bit PCM little‑endian at 16‑kHz
                    await client_ws.send(msg)
            except WebSocketDisconnect:
                await client_ws.close()

        async def forward_openai_to_browser():
            try:
                async for msg in client_ws.iter_bytes():
                    # Relay OpenAI audio bytes directly
                    await ws.send_bytes(msg)
            except Exception:
                await ws.close()

        forward_tasks = [
            asyncio.create_task(forward_browser_to_openai()),
            asyncio.create_task(forward_openai_to_browser()),
        ]
        done, pending = await asyncio.wait(forward_tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()

def parse_arguments():
    parser = argparse.ArgumentParser(description='{} {} parse argument'.format(__file__, __name__))
    
    ### DEBUG
    parser.add_argument('-d', action='store_true',help='Wait for debuggee attach')   
    parser.add_argument('-debug', type=bool, default=False, help='Wait for debuggee attach')
    parser.add_argument('-debug_port', type=int, default=3000, help='Debug port')
    parser.add_argument('-debug_address', type=str, default='0.0.0.0', help='Debug port')
    parser.add_argument('-server_port', type=int, default=5000, help='Debug port')
    parser.add_argument('-min', action='store_true', help='Load minimal data for development')
    parser.add_argument('-min_cycles', type=int, default=25, help='Number of cycles for min')
    
    ### CREDS
    parser.add_argument('-creds', type=str, default='config/creds.yaml', help='Credentials file')
    parser.add_argument('-api', type=str, default='AzureOpenaiDev', help='Credentials file')



    args = parser.parse_args()
    if args.d:
        args.debug = args.d

    return args

def main(args): # Renamed args to args_main to avoid conflict
    global obj_retrieval

    # app.run(host=\'0.0.0.0\', port=args.server_port, debug=False, threaded=True) # Flask way
    uvicorn.run(app, host="0.0.0.0", port=args.server_port)


if __name__ == '__main__':

    args = parse_arguments()

    if args.debug:
        print("Wait for debugger attach on {}:{}".format(args.debug_address, args.debug_port))
        import debugpy

        debugpy.listen(address=(args.debug_address, args.debug_port)) # Pause the program until a remote debugger is attached
        debugpy.wait_for_client() # Pause the program until a remote debugger is attached
        print("Debugger attached")

    main(args)