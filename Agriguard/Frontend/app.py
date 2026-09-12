import streamlit as st
import requests


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="AgriGuard",
    page_icon="🌱"
)


st.title("🌱 AgriGuard")

st.write(
    "AI-powered crop disease screening"
)


# =========================================================
# CROP
# =========================================================

crop = st.selectbox(
    "Select crop",
    [
        "Tomato",
        "Potato",
        "Bell Pepper",
        "Grape"
    ]
)


# =========================================================
# IMAGE
# =========================================================

uploaded_file = st.file_uploader(
    "Upload a crop leaf image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


# =========================================================
# CONDITIONS
# =========================================================

st.subheader(
    "🌦️ Current Conditions"
)


humidity = st.slider(
    "Humidity (%)",
    0,
    100,
    70
)


temperature = st.number_input(
    "Temperature (°C)",
    min_value=0.0,
    max_value=60.0,
    value=25.0
)


rain = st.checkbox(
    "Recent rain / wet conditions"
)


# =========================================================
# ANALYZE
# =========================================================

if uploaded_file:

    st.image(
        uploaded_file,
        caption="Uploaded leaf",
        use_container_width=True
    )


    if st.button(
        "🔍 Analyze Crop",
        use_container_width=True
    ):

        with st.spinner(
            "Gemini is analyzing the crop..."
        ):

            files = {

                "file": (

                    uploaded_file.name,

                    uploaded_file.getvalue(),

                    uploaded_file.type
                )
            }


            data = {

                "crop":
                    crop,

                "humidity":
                    humidity,

                "temperature":
                    temperature,

                "rain":
                    rain
            }


            response = requests.post(

                "http://127.0.0.1:8000/analyze",

                files=files,

                data=data,

                timeout=90
            )


        # =================================================
        # HANDLE RESPONSE
        # =================================================

        if response.status_code != 200:

            st.error(
                "Gemini analysis failed."
            )

            st.code(
                response.text
            )

        else:

            result = response.json()


            # =================================================
            # DIAGNOSIS
            # =================================================

            st.divider()

            st.header(
                "🔬 AI Diagnosis"
            )


            st.success(
                result["disease"]
            )


            st.metric(
                "AI Confidence",
                f"{result['confidence']:.1%}"
            )


            # =================================================
            # RISK
            # =================================================

            st.header(
                "🚨 Risk Level"
            )


            risk = result[
                "risk_level"
            ]


            score = result[
                "risk_score"
            ]


            if risk == "HIGH":

                st.error(
                    f"🔴 HIGH RISK — "
                    f"{score}/100"
                )


            elif risk == "MEDIUM":

                st.warning(
                    f"🟡 MEDIUM RISK — "
                    f"{score}/100"
                )


            elif risk == "LOW":

                st.success(
                    f"🟢 LOW RISK — "
                    f"{score}/100"
                )


            else:

                st.warning(
                    "⚠️ UNCERTAIN"
                )


            # =================================================
            # REASONING
            # =================================================

            st.subheader(
                "🧠 Why?"
            )

            st.write(
                result["reasoning"]
            )


            # =================================================
            # SYMPTOMS
            # =================================================

            st.header(
                "🔎 Possible Symptoms"
            )


            for symptom in result[
                "symptoms"
            ]:

                st.write(
                    f"• {symptom}"
                )


            # =================================================
            # ACTIONS
            # =================================================

            st.header(
                "🌱 Recommended Actions"
            )


            for action in result[
                "recommended_actions"
            ]:

                st.write(
                    f"✅ {action}"
                )


            # =================================================
            # PREVENTION
            # =================================================

            st.header(
                "🛡️ Prevention"
            )


            for item in result[
                "prevention"
            ]:

                st.write(
                    f"• {item}"
                )


            # =================================================
            # DISCLAIMER
            # =================================================

            st.info(
                "AgriGuard provides preliminary "
                "AI-based crop screening and "
                "decision support. Confirm important "
                "treatment decisions with qualified "
                "local agricultural guidance."
            )