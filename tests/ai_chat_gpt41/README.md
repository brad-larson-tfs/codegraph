Real‑time voice chat demo that proxies the [GPT‑4o Realtime API](https://platform.openai.com/docs/guides/realtime/realtime-api-beta) through a FastAPI WebSocket.

## Quick start
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # edit your API key & model
uvicorn main:app --reload
```
Visit `http://localhost:8000`, click the round microphone button, and start talking!

## How it works
1. **Browser** captures 16‑kHz mono audio → sends raw chunks to `/ws/{session_id}`.
2. **FastAPI** opens a parallel WS connection to OpenAI’s realtime endpoint and pipes audio both ways.
3. OpenAI streams synthesized audio back; server relays to browser which plays it immediately using Web Audio API.
4. Conversation text (optional) is kept per‑session in memory; extend with database for long‑term storage.

## Next steps / Improvements
- Persist histories to Postgres/Redis.
- Transcribe with Whisper to display text chat bubbles.
- Handle back‑pressure (pause recording when OpenAI responds).
- Use Service Workers for offline caching.
- Secure with OAuth2 and rate‑limit.