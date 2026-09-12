def calculate_risk(
    disease_info,
    confidence,
    humidity,
    rain,
    temperature
):

    # =========================================================
    # 1. DISEASE SEVERITY
    # =========================================================

    severity = disease_info["severity"]

    severity_score = (
        severity / 5
    ) * 30


    # =========================================================
    # 2. AI CONFIDENCE
    # =========================================================

    confidence_score = (
        confidence * 25
    )


    # =========================================================
    # 3. HUMIDITY
    # =========================================================

    environment = disease_info["environment"]

    humidity_threshold = environment[
        "humidity_threshold"
    ]

    if humidity >= humidity_threshold:

        humidity_score = 20

    elif humidity >= humidity_threshold - 10:

        humidity_score = 10

    else:

        humidity_score = 0


    # =========================================================
    # 4. RAIN
    # =========================================================

    if (
        rain
        and environment["rain_increases_risk"]
    ):

        rain_score = 15

    else:

        rain_score = 0


    # =========================================================
    # 5. TEMPERATURE
    # =========================================================

    minimum_temp, maximum_temp = (
        environment["temperature_range"]
    )

    if (
        minimum_temp
        <= temperature
        <= maximum_temp
    ):

        temperature_score = 10

    else:

        temperature_score = 0


    # =========================================================
    # 6. TOTAL SCORE
    # =========================================================

    score = (
        severity_score
        + confidence_score
        + humidity_score
        + rain_score
        + temperature_score
    )


    score = min(
        round(score, 1),
        100
    )


    # =========================================================
    # 7. LOW CONFIDENCE SAFETY CHECK
    # =========================================================

    if confidence < 0.55:

        level = "UNCERTAIN"


    elif score >= 70:

        level = "HIGH"


    elif score >= 40:

        level = "MEDIUM"


    else:

        level = "LOW"


    # =========================================================
    # 8. EXPLANATION
    # =========================================================

    reasons = []


    if confidence >= 0.80:

        reasons.append(
            "AI prediction confidence is high"
        )

    elif confidence < 0.55:

        reasons.append(
            "AI prediction confidence is low"
        )


    if humidity >= humidity_threshold:

        reasons.append(
            "Humidity is favorable for this disease"
        )


    if rain and environment[
        "rain_increases_risk"
    ]:

        reasons.append(
            "Wet conditions may increase disease risk"
        )


    if (
        minimum_temp
        <= temperature
        <= maximum_temp
    ):

        reasons.append(
            "Current temperature is within "
            "the model's favorable range"
        )


    return {

        "score": score,

        "level": level,

        "reasons": reasons
    }