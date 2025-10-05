const container = document.getElementById("recordingsContainer");

async function loadRecordings() {
  try {
    const response = await fetch("http://localhost:8000/api/list-recordings");
    if (!response.ok) throw new Error("Failed to fetch recordings");
    const recordings = await response.json();

    if (recordings.length === 0) {
      container.innerHTML = "<p>No recordings found.</p>";
      return;
    }

    container.innerHTML = ""; // Clear existing content

    recordings.forEach((rec) => {
      const card = document.createElement("div");
      card.className = "recording-card";

      const audio = document.createElement("audio");
      audio.controls = true;
      audio.src = rec.file_path.startsWith("/")
                ? `http://localhost:8000${rec.file_path}`
                : `http://localhost:8000/${rec.file_path}`;


      const transcript = document.createElement("p");
      transcript.textContent = rec.transcript
        ? `Transcript: ${rec.transcript}`
        : "No transcript provided.";

      const timestamp = document.createElement("p");
      timestamp.textContent = `Saved: ${rec.timestamp || "Unknown"}`;

      card.appendChild(audio);
      card.appendChild(transcript);
      card.appendChild(timestamp);

      container.appendChild(card);
    });
  } catch (error) {
    console.error(error);
    container.innerHTML = "<p>Error loading recordings.</p>";
  }
}

loadRecordings();
 