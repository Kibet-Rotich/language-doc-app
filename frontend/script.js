let mediaRecorder;
let recordedChunks = [];
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const audioPreview = document.getElementById("audioPreview");
const uploadForm = document.getElementById("uploadForm");
const statusMsg = document.getElementById("status");

startBtn.addEventListener("click", async () => {
  recordedChunks = [];
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) {
        recordedChunks.push(e.data);
      }
    };

    mediaRecorder.onstop = () => {
      const blob = new Blob(recordedChunks, { type: "audio/webm" });
      audioPreview.src = URL.createObjectURL(blob);
    };

    mediaRecorder.start();
    startBtn.disabled = true;
    stopBtn.disabled = false;
    statusMsg.textContent = "Recording...";
  } catch (err) {
    console.error("Error accessing microphone:", err);
    statusMsg.textContent = "Microphone access denied or unavailable.";
  }
});

stopBtn.addEventListener("click", () => {
  mediaRecorder.stop();
  startBtn.disabled = false;
  stopBtn.disabled = true;
  statusMsg.textContent = "Recording stopped. You can preview and upload.";
});

uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!recordedChunks.length) {
    statusMsg.textContent = "No recording to upload.";
    return;
  }

  const blob = new Blob(recordedChunks, { type: "audio/webm" });
  const formData = new FormData();
  const transcript = document.getElementById("transcript").value;
  formData.append("file", blob, "recording.webm");
  formData.append("transcript", transcript);

  statusMsg.textContent = "Uploading...";

  try {
    const response = await fetch("http://localhost:8000/api/upload-audio", {
      method: "POST",
      body: formData
    });
    if (!response.ok) throw new Error("Upload failed");
    const result = await response.json();
    statusMsg.textContent = `Upload success! ID: ${result.id}`;
  } catch (error) {
    console.error(error);
    statusMsg.textContent = "Error uploading audio.";
  }
});
