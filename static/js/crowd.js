async function updateCrowdCount(delta) {
  if (typeof window.CROWD_EVENT_ID === "undefined") {
    return;
  }

  try {
    const response = await fetch(
      `/api/events/${window.CROWD_EVENT_ID}/update_count`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ delta }),
      }
    );

    if (!response.ok) {
      throw new Error("Failed to update count");
    }

    const data = await response.json();
    applyEventState(data);
  } catch (err) {
    console.error(err);
  }
}

async function refreshEventState() {
  if (typeof window.CROWD_EVENT_ID === "undefined") {
    return;
  }

  try {
    const response = await fetch(`/api/events/${window.CROWD_EVENT_ID}`);
    if (!response.ok) {
      throw new Error("Failed to fetch event");
    }
    const data = await response.json();
    applyEventState(data);
  } catch (err) {
    console.error(err);
  }
}

function applyEventState(event) {
  const countEl = document.getElementById("current-count");
  const percentEl = document.getElementById("occupancy-percent");
  const barEl = document.getElementById("occupancy-bar");
  const statusChip = document.getElementById("status-chip");
  const statusLabel = document.getElementById("status-label");
  const statusMessage = document.getElementById("status-message");

  if (!countEl || !percentEl || !barEl || !statusChip) {
    return;
  }

  countEl.textContent = event.current_count;
  percentEl.textContent = event.occupancy_percent;
  barEl.style.width = `${event.occupancy_percent}%`;

  // Reset status classes
  barEl.classList.remove("status-normal", "status-warning", "status-critical");
  statusChip.classList.remove(
    "status-normal",
    "status-warning",
    "status-critical"
  );

  const status = event.status || "normal";
  barEl.classList.add(`status-${status}`);
  statusChip.classList.add(`status-${status}`);

  if (statusLabel) {
    statusLabel.textContent = status.charAt(0).toUpperCase() + status.slice(1);
  }
  if (statusMessage && event.status_message) {
    statusMessage.textContent = event.status_message;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const entryBtn = document.getElementById("btn-entry");
  const exitBtn = document.getElementById("btn-exit");

  if (entryBtn) {
    entryBtn.addEventListener("click", () => updateCrowdCount(1));
  }
  if (exitBtn) {
    exitBtn.addEventListener("click", () => updateCrowdCount(-1));
  }

  if (typeof window.CROWD_EVENT_ID !== "undefined") {
    // Periodically refresh in case multiple gates are updating at once
    setInterval(refreshEventState, 4000);
  }
});

