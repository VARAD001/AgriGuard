from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from Backend.gemini_service import analyze_crop
import traceback

app = FastAPI(title="AgriGuard API")


# =========================================================
# STATIC FRONTEND (index.html, style.css, script.js)
# =========================================================

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")


# =========================================================
# ANALYZE ENDPOINT
# =========================================================

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    crop: str = Form("Unknown"),
    humidity: float = Form(70),
    temperature: float = Form(25),
    rain: bool = Form(False)
):
    try:
        print("\n==============================")
        print("NEW REQUEST")
        print("Filename:", file.filename)
        print("Content type:", file.content_type)
        print("Crop:", crop)
        print("Humidity:", humidity)
        print("Temperature:", temperature)
        print("Rain:", rain)

        image_bytes = await file.read()

        print("Image bytes:", len(image_bytes))

        if not image_bytes:
            raise ValueError("Uploaded image is empty")

        result = analyze_crop(
            image_bytes=image_bytes,
            mime_type=file.content_type or "image/jpeg",
            crop=crop,
            humidity=humidity,
            temperature=temperature,
            rain=rain
        )

        print("Gemini response received")

        return result.model_dump()

    except Exception as e:
        print("\n========== BACKEND ERROR ==========")
        traceback.print_exc()
        print("====================================\n")

        return JSONResponse(
            status_code=500,
            content={"error": str(e), "error_type": type(e).__name__}
        )
