const form = document.getElementById("analyze-form");
const analyzeBtn = document.getElementById("analyze-btn");
const btnLabel = analyzeBtn.querySelector(".btn-label");
const btnSpinner = analyzeBtn.querySelector(".btn-spinner");

const imageInput = document.getElementById("image-input");
const dropzone = document.getElementById("dropzone");
const dropzoneEmpty = document.getElementById("dropzone-empty");
const dropzonePreview = document.getElementById("dropzone-preview");
const previewImg = document.getElementById("preview-img");
const removeImageBtn = document.getElementById("remove-image");

const humidityInput = document.getElementById("humidity");
const humidityValue = document.getElementById("humidity-value");
const temperatureInput = document.getElementById("temperature");
const temperatureValue = document.getElementById("temperature-value");

const locateBtn = document.getElementById("locate-btn");
const locateLabel = document.getElementById("locate-label");

const emptyState = document.getElementById("empty-state");
const errorState = document.getElementById("error-state");
const errorMessage = document.getElementById("error-message");
const report = document.getElementById("report");

// Fertilizer planner elements
const fertForm = document.getElementById("fert-form");
const fertBtn = document.getElementById("fert-btn");
const fertBtnLabel = fertBtn.querySelector(".btn-label");
const fertBtnSpinner = fertBtn.querySelector(".btn-spinner");
const plantCropSelect = document.getElementById("plant-crop");

const shcInput = document.getElementById("shc-input");
const shcDropzone = document.getElementById("shc-dropzone");
const shcDropzoneEmpty = document.getElementById("shc-dropzone-empty");
const shcDropzonePreview = document.getElementById("shc-dropzone-preview");
const shcPreviewImg = document.getElementById("shc-preview-img");
const shcRemoveImageBtn = document.getElementById("shc-remove-image");

const fertilizerReport = document.getElementById("fertilizer-report");

let selectedFile = null;
let selectedShcFile = null;

// ---------------------------------------------------
// SLIDERS
// ---------------------------------------------------

humidityInput.addEventListener("input", () => {
  humidityValue.textContent = `${humidityInput.value}%`;
});

temperatureInput.addEventListener("input", () => {
  temperatureValue.textContent = `${temperatureInput.value}°C`;
});

// ---------------------------------------------------
// LOCATION-BASED CONDITIONS
// ---------------------------------------------------

locateBtn.addEventListener("click", () => {
  if (!navigator.geolocation) {
    locateLabel.textContent = "Location not supported here";
    return;
  }

  locateBtn.disabled = true;
  locateLabel.textContent = "Locating…";

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const { latitude, longitude } = position.coords;

      try {
        const url = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,relative_humidity_2m`;
        const res = await fetch(url);

        if (!res.ok) throw new Error("Weather lookup failed");

        const data = await res.json();
        const temp = Math.round(data.current.temperature_2m);
        const humidity = Math.round(data.current.relative_humidity_2m);

        temperatureInput.value = temp;
        temperatureValue.textContent = `${temp}°C`;

        humidityInput.value = humidity;
        humidityValue.textContent = `${humidity}%`;

        locateLabel.textContent = "Updated from your location";
      } catch (err) {
        locateLabel.textContent = "Couldn't fetch weather — try again";
      } finally {
        locateBtn.disabled = false;
      }
    },
    (error) => {
      locateLabel.textContent =
        error.code === error.PERMISSION_DENIED
          ? "Location permission denied"
          : "Couldn't get your location";
      locateBtn.disabled = false;
    },
    { timeout: 8000 }
  );
});

// ---------------------------------------------------
// DROPZONE — leaf specimen
// ---------------------------------------------------

dropzone.addEventListener("click", () => imageInput.click());

dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("dragover");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("dragover");
});

dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.classList.remove("dragover");
  if (e.dataTransfer.files.length) {
    setFile(e.dataTransfer.files[0]);
  }
});

imageInput.addEventListener("change", () => {
  if (imageInput.files.length) {
    setFile(imageInput.files[0]);
  }
});

removeImageBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  clearFile();
});

function setFile(file) {
  if (!file.type.startsWith("image/")) return;
  selectedFile = file;

  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    dropzoneEmpty.hidden = true;
    dropzonePreview.hidden = false;
  };
  reader.readAsDataURL(file);

  analyzeBtn.disabled = false;
}

function clearFile() {
  selectedFile = null;
  imageInput.value = "";
  dropzoneEmpty.hidden = false;
  dropzonePreview.hidden = true;
  analyzeBtn.disabled = true;
}

// ---------------------------------------------------
// DROPZONE — soil health card
// ---------------------------------------------------

shcDropzone.addEventListener("click", () => shcInput.click());

shcDropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  shcDropzone.classList.add("dragover");
});

shcDropzone.addEventListener("dragleave", () => {
  shcDropzone.classList.remove("dragover");
});

shcDropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  shcDropzone.classList.remove("dragover");
  if (e.dataTransfer.files.length) {
    setShcFile(e.dataTransfer.files[0]);
  }
});

shcInput.addEventListener("change", () => {
  if (shcInput.files.length) {
    setShcFile(shcInput.files[0]);
  }
});

shcRemoveImageBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  clearShcFile();
});

function setShcFile(file) {
  if (!file.type.startsWith("image/")) return;
  selectedShcFile = file;

  const reader = new FileReader();
  reader.onload = (e) => {
    shcPreviewImg.src = e.target.result;
    shcDropzoneEmpty.hidden = true;
    shcDropzonePreview.hidden = false;
  };
  reader.readAsDataURL(file);

  fertBtn.disabled = false;
}

function clearShcFile() {
  selectedShcFile = null;
  shcInput.value = "";
  shcDropzoneEmpty.hidden = false;
  shcDropzonePreview.hidden = true;
  fertBtn.disabled = true;
}

// ---------------------------------------------------
// SUBMIT — crop disease screening
// ---------------------------------------------------

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!selectedFile) return;

  setLoading(true);
  errorState.hidden = true;
  emptyState.hidden = true;

  const formData = new FormData();
  formData.append("file", selectedFile);
  formData.append("crop", document.getElementById("crop").value);
  formData.append("humidity", humidityInput.value);
  formData.append("temperature", temperatureInput.value);
  formData.append("rain", document.getElementById("rain").checked);

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (!response.ok || result.error) {
      showError(result.error || "The server returned an unexpected error.");
    } else {
      renderReport(result, previewImg.src);
    }
  } catch (err) {
    showError("Couldn't reach the analysis server. Check that the backend is running.");
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  analyzeBtn.disabled = isLoading || !selectedFile;
  btnSpinner.hidden = !isLoading;
  btnLabel.textContent = isLoading ? "Analyzing…" : "Analyze specimen";
}

// ---------------------------------------------------
// SUBMIT — fertilizer planner
// ---------------------------------------------------

fertForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!selectedShcFile) return;

  setFertLoading(true);
  errorState.hidden = true;
  emptyState.hidden = true;

  const formData = new FormData();
  formData.append("file", selectedShcFile);
  formData.append("crop", plantCropSelect.value);

  try {
    const response = await fetch("/fertilizer-plan", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (!response.ok || result.error) {
      showError(result.error || "The server returned an unexpected error.");
    } else {
      renderFertilizerReport(result);
    }
  } catch (err) {
    showError("Couldn't reach the analysis server. Check that the backend is running.");
  } finally {
    setFertLoading(false);
  }
});

function setFertLoading(isLoading) {
  fertBtn.disabled = isLoading || !selectedShcFile;
  fertBtnSpinner.hidden = !isLoading;
  fertBtnLabel.textContent = isLoading ? "Analyzing…" : "Get fertilizer plan";
}

// ---------------------------------------------------
// SHARED ERROR STATE
// ---------------------------------------------------

function showError(message) {
  report.hidden = true;
  fertilizerReport.hidden = true;
  emptyState.hidden = true;
  errorState.hidden = false;
  errorMessage.textContent = message;
}

// ---------------------------------------------------
// RENDER — disease report
// ---------------------------------------------------

function renderReport(result, photoSrc) {
  errorState.hidden = true;
  emptyState.hidden = true;
  fertilizerReport.hidden = true;
  report.hidden = false;

  document.getElementById("report-crop").textContent = result.crop || "—";
  document.getElementById("report-disease").textContent = result.disease;
  document.getElementById("report-photo").src = photoSrc;
  document.getElementById("report-reasoning").textContent = result.reasoning;

  // confidence ring
  const circumference = 2 * Math.PI * 30;
  const pct = Math.max(0, Math.min(1, result.confidence));
  const arc = document.getElementById("confidence-arc");
  arc.style.strokeDasharray = `${circumference}`;
  arc.style.strokeDashoffset = `${circumference * (1 - pct)}`;
  document.getElementById("confidence-value").textContent = `${Math.round(pct * 100)}%`;

  // risk gauge
  const score = Math.max(0, Math.min(100, result.risk_score));
  document.getElementById("gauge-fill").style.width = `${score}%`;
  document.getElementById("gauge-marker").style.left = `calc(${score}% - 1.5px)`;

  const riskCaption = document.getElementById("risk-caption");
  const riskCaptions = {
    LOW: `Low risk — ${score}/100`,
    MEDIUM: `Medium risk — ${score}/100`,
    HIGH: `High risk — ${score}/100`,
    UNCERTAIN: "Risk level uncertain",
  };
  riskCaption.textContent = riskCaptions[result.risk_level] || "Risk level uncertain";

  const riskColors = { LOW: "var(--moss-soft)", MEDIUM: "var(--ochre)", HIGH: "var(--rust)" };
  riskCaption.style.color = riskColors[result.risk_level] || "var(--ink-soft)";

  // lists
  fillList("report-symptoms", result.symptoms);
  fillList("report-actions", result.recommended_actions);
  fillList("report-prevention", result.prevention);
}

function fillList(id, items) {
  const el = document.getElementById(id);
  el.innerHTML = "";
  (items || []).forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    el.appendChild(li);
  });
}

// ---------------------------------------------------
// RENDER — fertilizer report
// ---------------------------------------------------

function renderFertilizerReport(result) {
  errorState.hidden = true;
  emptyState.hidden = true;
  report.hidden = true;
  fertilizerReport.hidden = false;

  document.getElementById("fert-crop").textContent = result.target_crop || "—";
  document.getElementById("fert-soil-summary").textContent = result.soil_summary;

  renderFertGrid(result.recommendations);
}

function renderFertGrid(items) {
  const el = document.getElementById("fert-grid");
  el.innerHTML = "";

  const sorted = [...(items || [])].sort((a, b) => a.priority - b.priority);

  sorted.forEach((item) => {
    const card = document.createElement("div");
    card.className = "fert-card";

    const rank = document.createElement("div");
    rank.className = "fert-rank";
    rank.textContent = item.priority;

    const body = document.createElement("div");
    body.className = "fert-body";

    const name = document.createElement("h4");
    name.textContent = item.name;

    const reason = document.createElement("p");
    reason.className = "fert-reason";
    reason.textContent = item.reason;

    const notes = document.createElement("p");
    notes.className = "fert-notes";
    notes.textContent = item.application_notes;

    body.appendChild(name);
    body.appendChild(reason);
    body.appendChild(notes);

    card.appendChild(rank);
    card.appendChild(body);

    el.appendChild(card);
  });
}
