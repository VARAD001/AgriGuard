recommendations = {

    "Tomato___Early_blight": {

        "crop": "Tomato",

        "risk": "HIGH",

        "symptoms": [
            "Dark spots on leaves",
            "Yellowing around infected areas"
        ],

        "actions": [
            "Remove severely infected leaves",
            "Improve air circulation",
            "Avoid overhead watering",
            "Monitor nearby plants"
        ],

        "prevention": [
            "Maintain proper plant spacing",
            "Keep leaves dry",
            "Remove infected plant material"
        ]
    },


    "Tomato___Late_blight": {

        "crop": "Tomato",

        "risk": "HIGH",

        "symptoms": [
            "Dark irregular lesions",
            "Rapid leaf damage",
            "Brown or black patches"
        ],

        "actions": [
            "Remove severely affected leaves",
            "Improve airflow",
            "Avoid overhead irrigation",
            "Monitor surrounding plants"
        ],

        "prevention": [
            "Avoid prolonged leaf wetness",
            "Maintain good plant spacing"
        ]
    },


    "Potato___Early_blight": {

        "crop": "Potato",

        "risk": "HIGH",

        "symptoms": [
            "Dark circular spots",
            "Yellowing leaves"
        ],

        "actions": [
            "Remove severely infected foliage",
            "Improve field ventilation",
            "Avoid overhead watering"
        ],

        "prevention": [
            "Maintain crop hygiene",
            "Monitor surrounding plants"
        ]
    },


    "Pepper__bell___Bacterial_spot": {

        "crop": "Bell Pepper",

        "risk": "MEDIUM",

        "symptoms": [
            "Small dark spots",
            "Leaf damage",
            "Spots on fruit"
        ],

        "actions": [
            "Remove severely infected leaves",
            "Avoid working with wet plants",
            "Improve airflow"
        ],

        "prevention": [
            "Use clean planting material",
            "Avoid overhead irrigation"
        ]
    }
}


def get_recommendation(disease):

    return recommendations.get(
        disease,
        {
            "crop": "Unknown",
            "risk": "UNKNOWN",
            "symptoms": [
                "Unable to provide reliable symptoms"
            ],
            "actions": [
                "Please capture a clearer image",
                "Consider consulting an agricultural expert"
            ],
            "prevention": []
        }
    )