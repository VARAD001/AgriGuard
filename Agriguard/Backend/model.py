from transformers import pipeline

# Load pretrained plant disease AI model
classifier = pipeline(
    "image-classification",
    model="Kathir56/plant-disease-tamilnadu"
)


def predict_disease(image):
    results = classifier(image)

    best_result = results[0]

    return {
        "disease": best_result["label"],
        "confidence": float(best_result["score"])
    }