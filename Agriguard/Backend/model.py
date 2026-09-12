from transformers import pipeline


# Load pretrained plant disease classifier
classifier = pipeline(
    "image-classification",
    model="Kathir56/plant-disease-tamilnadu"
)


def predict_disease(image):

    results = classifier(
        image,
        top_k=3
    )

    best = results[0]

    return {
        "disease": best["label"],
        "confidence": float(best["score"]),

        "alternatives": [
            {
                "disease": item["label"],
                "confidence": float(item["score"])
            }
            for item in results
        ]
    }