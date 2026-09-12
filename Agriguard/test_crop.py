from Backend.gemini_service import analyze_crop


with open(
    "leaf.jpg",
    "rb"
) as file:

    image_bytes = file.read()


result = analyze_crop(

    image_bytes=image_bytes,

    mime_type="image/jpeg",

    crop="Tomato",

    humidity=85,

    temperature=27,

    rain=True
)


print(
    result.model_dump_json(
        indent=2
    )
)