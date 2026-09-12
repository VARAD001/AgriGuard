import streamlit as st
import requests


st.set_page_config(
    page_title="AgriGuard",
    page_icon="🌱",
    layout="centered"
)


st.title("🌱 AgriGuard")

st.write(
    "AI-powered crop disease screening and recommendations"
)


# Upload image
uploaded_file = st.file_uploader(
    "Upload a photo of the affected leaf",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    # Display image
    st.image(
        uploaded_file,
        caption="Uploaded leaf",
        use_container_width=True
    )


    # Analyze button
    if st.button(
        "🔍 Analyze Crop",
        use_container_width=True
    ):

        with st.spinner("Analyzing your crop..."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }


            # Send image to FastAPI
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                files=files
            )


        # Check response
        if response.status_code == 200:

            result = response.json()


            # -------------------------
            # DISEASE
            # -------------------------

            disease = result["disease"]

            confidence = result["confidence"]


            # Make disease name readable
            disease_display = (
                disease
                .replace("___", " - ")
                .replace("__", " - ")
                .replace("_", " ")
            )


            st.success(
                f"🌿 Disease detected: {disease_display}"
            )


            st.metric(
                "AI Confidence",
                f"{confidence:.1%}"
            )


            # -------------------------
            # RECOMMENDATION
            # -------------------------

            recommendation = result[
                "recommendation"
            ]


            st.subheader("⚠️ Risk Level")

            risk = recommendation["risk"]


            if risk == "HIGH":

                st.error(f"🔴 {risk}")

            elif risk == "MEDIUM":

                st.warning(f"🟡 {risk}")

            else:

                st.info(f"🟢 {risk}")


            # -------------------------
            # SYMPTOMS
            # -------------------------

            st.subheader("🔎 Possible Symptoms")

            for symptom in recommendation["symptoms"]:

                st.write(
                    f"• {symptom}"
                )


            # -------------------------
            # ACTIONS
            # -------------------------

            st.subheader("🌱 Recommended Actions")

            for action in recommendation["actions"]:

                st.write(
                    f"✅ {action}"
                )


            # -------------------------
            # PREVENTION
            # -------------------------

            st.subheader("🛡️ Prevention")

            for item in recommendation["prevention"]:

                st.write(
                    f"• {item}"
                )


            st.info(
                "AgriGuard provides preliminary "
                "AI-based screening. Confirm important "
                "treatment decisions with local agricultural "
                "guidance."
            )


        else:

            st.error(
                "Something went wrong while "
                "analyzing the image."
            )