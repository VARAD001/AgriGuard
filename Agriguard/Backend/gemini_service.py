import base64
from typing import List, Literal

from google import genai
from pydantic import BaseModel, Field


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client()


# =========================================================
# STRUCTURED OUTPUT SCHEMA
# =========================================================

class CropAnalysis(BaseModel):

    crop: str = Field(
        description="Most likely crop visible in the image"
    )

    disease: str = Field(
        description="Most likely plant disease or Healthy"
    )

    confidence: float = Field(
        description="Estimated confidence from 0.0 to 1.0"
    )

    risk_level: Literal[
        "LOW",
        "MEDIUM",
        "HIGH",
        "UNCERTAIN"
    ]

    risk_score: int = Field(
        description="Risk score from 0 to 100"
    )

    symptoms: List[str] = Field(
        description="Visible or characteristic symptoms"
    )

    recommended_actions: List[str] = Field(
        description="Immediate practical actions"
    )

    prevention: List[str] = Field(
        description="Prevention and monitoring steps"
    )

    reasoning: str = Field(
        description="Short explanation of the diagnosis and risk"
    )

def analyze_crop(
    image_bytes: bytes,
    mime_type: str,
    crop: str,
    humidity: float,
    temperature: float,
    rain: bool
):

    # Convert image → base64
    image_base64 = base64.b64encode(
        image_bytes
    ).decode("utf-8")


    prompt = f"""
You are AgriGuard, an agricultural crop-health
decision-support assistant.

Analyze the supplied crop leaf image.

Known user-provided context:

Crop selected by user:
{crop}

Humidity:
{humidity}%

Temperature:
{temperature}°C

Recent rain / wet conditions:
{rain}


TASK

1. Identify the most likely disease visible in the image.
2. Estimate confidence from 0.0 to 1.0.
3. Estimate a risk level:
   LOW, MEDIUM, HIGH, or UNCERTAIN.
4. Produce a risk score from 0 to 100.
5. List possible symptoms.
6. Give practical recommended actions.
7. Give prevention steps.
8. Briefly explain why you reached the result.


IMPORTANT RULES

- Treat this as preliminary crop-health screening,
  not a definitive agricultural diagnosis.
- If the image is unclear, say UNCERTAIN.
- Do not invent certainty.
- Do not invent pesticide dosages.
- Do not recommend mixing chemicals.
- Prefer cultural/IPM actions such as monitoring,
  sanitation, airflow, irrigation management,
  removal of affected material, and appropriate
  agricultural guidance.
- If the selected crop conflicts with what is visible,
  mention the uncertainty.
- Keep the response practical for a farmer.
- Return ONLY the requested structured result.
"""


    interaction = client.interactions.create(

        model="gemini-3.8-flash",

        input=[

            {
                "type": "text",
                "text": prompt
            },

            {
                "type": "image",
                "data": image_base64,
                "mime_type": mime_type
            }
        ],

        response_format={

            "type": "text",

            "mime_type": "application/json",

            "schema":
                CropAnalysis.model_json_schema()
        }
    )


    # Convert Gemini JSON → Pydantic object
    result = CropAnalysis.model_validate_json(
        interaction.output_text
    )


    return result