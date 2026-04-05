from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from dotenv import load_dotenv
import asyncio

# --- Configuration ---
load_dotenv()
from obi_kaya_agent.agent import root_agent # Import your agent

APP_NAME = "obi_kaya_agent"

# --- ADK & FastAPI Setup ---
session_service = InMemorySessionService()
runner = Runner(app_name=APP_NAME, agent=root_agent, session_service=session_service)
app = FastAPI()

# --- HTML Frontend ---
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ObiKaya Terminal</title>
    <style>
        :root {
            --term-green: #00ff00;
            --term-dark: #001100;
            --term-bg: #000000;
        }
        body {
            background-color: var(--term-bg);
            color: var(--term-green);
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 20px;
            height: 100vh;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
        }
        #main-display {
            display: flex;
            flex-grow: 1;
            overflow: hidden;
            border: 2px solid var(--term-green);
            margin-bottom: 20px;
        }
        #chat-window {
            flex-grow: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        #avatar-display {
            width: 250px;
            border-left: 2px solid var(--term-green);
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
        }
        #avatar {
            width: 200px;
            height: 200px;
            image-rendering: pixelated;
            border: 1px solid var(--term-green);
            margin-bottom: 10px;
        }
        .message { white-space: pre-wrap; line-height: 1.4; }
        .user { color: #00ccff; }
        .aida { color: var(--term-green); }
        .system { opacity: 0.7; font-style: italic; }

        #input-area {
            display: flex;
            align-items: center;
            border: 2px solid var(--term-green);
            padding: 10px;
            font-size: 1.2rem;
        }
        #prompt-symbol { margin-right: 10px; }
        #user-input {
            flex-grow: 1;
            background: transparent;
            border: none;
            color: var(--term-green);
            font-family: inherit;
            font-size: inherit;
            outline: none;
        }
    </style>
</head>
<body>
    <div id="main-display">
        <div id="chat-window">
            <div class="message system">SYSTEM> ObiKaya Interface Loaded.</div>
        </div>
        <div id="avatar-display">
            <img id="avatar" src="/idle" alt="ObiKaya Avatar">
            <h3>ObiKaya-8000</h3>
        </div>
    </div>
    <form id="input-area">
        <span id="prompt-symbol">&gt;</span>
        <input type="text" id="user-input" autocomplete="off" autofocus>
    </form>

    <script>
        const chatWindow = document.getElementById('chat-window');
        const avatar = document.getElementById('avatar');
        const inputForm = document.getElementById('input-area');
        const userInput = document.getElementById('user-input');

        // --- Animation Control ---
        let talkInterval = null;

        function setAvatarState(state) {
            if (state === 'talking') {
                if (!talkInterval) {
                    // Simple toggle animation
                    talkInterval = setInterval(() => {
                        const isTalking = avatar.src.endsWith('/talk');
                        avatar.src = isTalking ? '/idle' : '/talk';
                    }, 150);
                }
            } else {
                // Idle state
                if (talkInterval) {
                    clearInterval(talkInterval);
                    talkInterval = null;
                }
                avatar.src = '/idle';
            }
        }

        // --- Message Handling ---
        function appendMessage(text, type) {
            const div = document.createElement('div');
            div.className = `message ${type}`;
            div.textContent = text;
            chatWindow.appendChild(div);
            chatWindow.scrollTop = chatWindow.scrollHeight;
            return div;
        }

        inputForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const query = userInput.value.trim();
            if (!query) return;

            appendMessage(`USER> ${query}`, 'user');
            userInput.value = '';

            // Prepare ObiKaya's message container
            const ObiKayaMsg = appendMessage('ObiKaya> ', 'aida');

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });

                const reader = response.body.getReader();
                const decoder = new TextDecoder();

                setAvatarState('talking');

                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;

                    const chunk = decoder.decode(value, { stream: true });
                    
                    // Typing effect
                    for (const char of chunk) {
                        ObiKayaMsg.textContent += char;
                        chatWindow.scrollTop = chatWindow.scrollHeight;
                        // Tiny delay for retro feel
                        await new Promise(r => setTimeout(r, 5)); 
                    }
                }
            } catch (err) {
                appendMessage(`SYSTEM> Error: ${err.message}`, 'system');
            } finally {
                setAvatarState('idle');
            }
        });
    </script>
</body>
</html>
"""

# --- Routes ---
@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML_CONTENT

@app.get("/idle")
async def get_idle_image():
    return FileResponse("static/assets/idle.png")

@app.get("/talk")
async def get_talk_image():
    return FileResponse("static/assets/talk.png")

# @app.post("/chat")
# async def chat_endpoint(request: Request):
#     data = await request.json()
#     user_query = data.get("query")
    
#     # Hardcoded for demo simplicity
#     user_id = "demo_user"
#     session_id = "demo_session"

#     # Ensure session exists
#     if not await session_service.get_session(APP_NAME, user_id, session_id):
#         await session_service.create_session(APP_NAME, user_id, session_id)

#     async def response_stream():
#         """Generates text chunks from the agent's events."""
#         async for event in runner.run_async(
#             user_id=user_id,
#             session_id=session_id,
#             new_message=Content(role="user", parts=[Part.from_text(text=user_query)]),
#         ):
#             # We only want the final text response for this simple UI
#             if event.is_final_response() and event.content and event.content.parts:
#                 for part in event.content.parts:
#                     if hasattr(part, "text") and part.text:
#                         yield part.text

#     return StreamingResponse(response_stream(), media_type="text/plain")

# @app.post("/chat")
# async def chat_endpoint(request: Request):
#     data = await request.json()
#     user_query = data.get("query")
    
#     # These IDs are used by the Runner to track state internally
#     user_id = "demo_user"
#     session_id = "demo_session"

#     async def response_stream():
#         """Generates text chunks from the agent's events."""
#         # The Runner automatically handles session retrieval/creation here!
#         async for event in runner.run_async(
#             user_id=user_id,
#             session_id=session_id,
#             new_message=Content(role="user", parts=[Part.from_text(text=user_query)]),
#         ):
#             # Check if this is the final text response
#             if event.is_final_response() and event.content and event.content.parts:
#                 for part in event.content.parts:
#                     if hasattr(part, "text") and part.text:
#                         yield part.text

#     return StreamingResponse(response_stream(), media_type="text/plain")

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_query = data.get("query")
    
    user_id = "demo_user"
    session_id = "demo_session"

    # --- RESTORE THIS BLOCK WITH KEYWORDS ---
    # We must explicitly name the arguments: app_name, user_id, and session_id
    session = await session_service.get_session(
        app_name=APP_NAME, 
        user_id=user_id, 
        session_id=session_id
    )
    
    if not session:
        await session_service.create_session(
            app_name=APP_NAME, 
            user_id=user_id, 
            session_id=session_id
        )
    # ----------------------------------------

    async def response_stream():
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=Content(role="user", parts=[Part.from_text(text=user_query)]),
        ):
            if event.is_final_response() and event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        yield part.text

    return StreamingResponse(response_stream(), media_type="text/plain")