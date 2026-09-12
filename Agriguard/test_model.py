from PIL import Image
from Backend.model import predict_disease


image = Image.open("leaf.jpg").convert("RGB")

result = predict_disease(image)

print(result)