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

class FertilizerItem(BaseModel):

    priority: int = Field(
        description="Priority rank starting at 1 (apply first)"
    )

    name: str = Field(
        description="Fertilizer, nutrient amendment, or soil input name"
    )

    reason: str = Field(
        description="Why this is recommended given the soil test values and the target crop"
    )

    application_notes: str = Field(
        description="General guidance on quantity/timing, grounded in the card's own reference values where available"
    )


class FertilizerPlan(BaseModel):

    target_crop: str = Field(
        description="The crop the farmer intends to plant"
    )

    soil_summary: str = Field(
        description="Brief summary of the soil health card findings relevant to this crop"
    )

    recommendations: List[FertilizerItem] = Field(
        description="Exactly four fertilizer recommendations, ordered by priority (1 = highest)"
    )


def recommend_fertilizers(
    image_bytes: bytes,
    mime_type: str,
    target_crop: str
):

    # Convert image → base64
    image_base64 = base64.b64encode(
        image_bytes
    ).decode("utf-8")


    prompt = f"""
You are AgriGuard, an agricultural crop-health
decision-support assistant.

Analyze the supplied Soil Health Card image. This is a
government-issued soil test report and typically includes:
pH, EC, organic carbon, available N/P/K, and available
sulphur/zinc/boron/iron/manganese/copper, each with a rating
(e.g. Low/Medium/High), plus a general recommendations section.

The farmer has NOT planted yet and intends to plant:
{target_crop}


TASK

1. Read and summarize the soil test values relevant to this crop.
2. Identify nutrient deficiencies or excesses that matter for
   this crop specifically.
3. Recommend EXACTLY four fertilizers or soil amendments to
   apply before planting, ordered by priority (1 = apply first).
4. For each, explain briefly why it's needed (tie it to a
   specific soil test value where possible).
5. Give general application notes (timing relative to planting,
   and quantity if the card itself provides a reference value
   for a similar crop/yield target — otherwise describe it in
   general terms rather than inventing an exact figure).


IMPORTANT RULES

- Treat this as preliminary decision support, not a replacement
  for official agricultural extension guidance.
- Ground any quantity you state in what is actually printed on
  the card, or in well-established general agronomic ranges.
  Do not invent precise dosages you cannot justify.
- Do not recommend mixing incompatible chemicals.
- Prefer addressing the most limiting nutrients first.
- If the image is unclear or not a soil health card, say so
  in soil_summary and give general, conservative guidance.
- Recommend the farmer confirm exact quantities with their
  local Krishi Vigyan Kendra / agricultural extension office
  before applying.
- Keep the response practical for a farmer.
- Return ONLY the requested structured result, with exactly
  four items in recommendations.
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
                FertilizerPlan.model_json_schema()
        }
    )


    result = FertilizerPlan.model_validate_json(
        interaction.output_text
    )


    return result


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