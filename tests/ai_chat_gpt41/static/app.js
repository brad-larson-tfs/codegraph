/* Client‑side JS – capture microphone, stream to server, play audio back */

const sessionId = crypto.randomUUID();
const chatEl = document.getElementById("chat");
const micBtn = document.getElementById("micBtn");
const micIcon = document.getElementById("micIcon");

let ws;
let mediaRecorder;
let audioContext;
let source;

function appendBubble(text, role) {
  const div = document.createElement("div");
  div.className = `bubble ${role}`;
  div.textContent = text;
  chatEl.appendChild(div);
  chatEl.scrollTop = chatEl.scrollHeight;
}

async function initWebSocket() {
  ws = new WebSocket(`${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws/${sessionId}`);
  ws.binaryType = "arraybuffer";

  ws.onmessage = async (event) => {
    // Received PCM audio bytes – decode and play
    const audioData = event.data;
    if (!audioContext) {
      audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
    }
    const arrayBuffer = await audioData.arrayBuffer?.() || audioData;
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
    const playSource = audioContext.createBufferSource();
    playSource.buffer = audioBuffer;
    playSource.connect(audioContext.destination);
    playSource.start(0);
  };

  ws.onclose = () => console.log("WebSocket closed");
}

async function startListening() {
  await initWebSocket();
  const stream = await navigator.mediaDevices.getUserMedia({ audio: { sampleRate: 16000, channelCount: 1 }, video: false });
  mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm;codecs=opus", audioBitsPerSecond: 128000 });

  mediaRecorder.addEventListener("dataavailable", (e) => {
    if (e.data.size > 0 && ws.readyState === WebSocket.OPEN) {
      e.data.arrayBuffer().then((buf) => ws.send(buf));
    }
  });

  mediaRecorder.start(250); // emit 250‑ms chunks
  micBtn.classList.add("listening");
}

function stopListening() {
  mediaRecorder?.stop();
  ws?.close();
  micBtn.classList.remove("listening");
}

micBtn.addEventListener("click", () => {
  if (micBtn.classList.contains("listening")) {
    stopListening();
  } else {
    startListening();
  }
});

// Optional: save conversation locally for persistence
window.addEventListener("beforeunload", () => {
  localStorage.setItem(`history-${sessionId}`, chatEl.innerHTML);
});

document.addEventListener("DOMContentLoaded", () => {
  const saved = localStorage.getItem(`history-${sessionId}`);
  if (saved) chatEl.innerHTML = saved;
});