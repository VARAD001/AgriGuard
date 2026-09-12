from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io

from Backend.model import predict_disease
from Backend.recommendations import get_recommendation


app = FastAPI(
    title="AgriGuard API"
)


@app.get("/")
def home():

    return {
        "message": "AgriGuard API is running"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Read uploaded image
    image_bytes = await file.read()

    # Convert bytes → PIL image
    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    # Send image to AI model
    prediction = predict_disease(image)

    # Get disease name
    disease = prediction["disease"]

    # Get recommendation
    recommendation = get_recommendation(disease)

    # Send everything back
    return {
        "disease": disease,
        "confidence": prediction["confidence"],
        "recommendation": recommendation
    }