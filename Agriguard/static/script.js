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

const emptyState = document.getElementById("empty-state");
const errorState = document.getElementById("error-state");
const errorMessage = document.getElementById("error-message");
const report = document.getElementById("report");

let selectedFile = null;

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
// DROPZONE
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
// SUBMIT
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

function showError(message) {
  report.hidden = true;
  emptyState.hidden = true;
  errorState.hidden = false;
  errorMessage.textContent = message;
}

// ---------------------------------------------------
// RENDER REPORT
// ---------------------------------------------------

function renderReport(result, photoSrc) {
  errorState.hidden = true;
  emptyState.hidden = true;
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
