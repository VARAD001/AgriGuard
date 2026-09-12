DISEASE_INFO = {

    # =========================================================
    # TOMATO EARLY BLIGHT
    # =========================================================

    "Tomato___Early_blight": {

        "crop": "Tomato",

        "display_name": "Tomato Early Blight",

        # 1 = low severity
        # 5 = very high severity
        "severity": 3,

        "symptoms": [
            "Small dark spots usually appear first on older leaves",
            "Brown spots may develop concentric ring patterns",
            "Yellowing can occur around infected spots",
            "Severely affected leaves may dry and fall"
        ],

        "actions": [
            "Remove severely affected leaves",
            "Improve airflow around the plants",
            "Keep foliage as dry as possible",
            "Monitor nearby plants for similar symptoms"
        ],

        "prevention": [
            "Maintain adequate spacing between plants",
            "Avoid unnecessary overhead watering",
            "Remove infected plant debris",
            "Scout plants regularly"
        ],

        # Conditions that increase concern
        "environment": {
            "humidity_threshold": 70,
            "rain_increases_risk": True,
            "temperature_range": (20, 30)
        }
    },


    # =========================================================
    # TOMATO LATE BLIGHT
    # =========================================================

    "Tomato___Late_blight": {

        "crop": "Tomato",

        "display_name": "Tomato Late Blight",

        "severity": 5,

        "symptoms": [
            "Large irregular dark lesions can develop on leaves",
            "Lesions may spread rapidly",
            "White growth can occur under humid conditions",
            "Stems and fruit can also become affected"
        ],

        "actions": [
            "Inspect surrounding plants immediately",
            "Remove severely affected plant material",
            "Keep foliage as dry as possible",
            "Monitor the crop closely for rapid disease spread"
        ],

        "prevention": [
            "Scout the crop frequently",
            "Avoid prolonged leaf wetness",
            "Maintain good spacing and airflow",
            "Remove infected plant debris"
        ],

        "environment": {
            "humidity_threshold": 75,
            "rain_increases_risk": True,
            "temperature_range": (15, 23)
        }
    },


    # =========================================================
    # TOMATO BACTERIAL SPOT
    # =========================================================

    "Tomato___Bacterial_spot": {

        "crop": "Tomato",

        "display_name": "Tomato Bacterial Spot",

        "severity": 4,

        "symptoms": [
            "Small brown circular spots can appear on leaves",
            "Yellow halos may surround leaf spots",
            "Spots can also appear on fruit",
            "Severe infections can cause extensive leaf damage"
        ],

        "actions": [
            "Remove severely affected leaves",
            "Avoid working with plants while they are wet",
            "Keep foliage as dry as possible",
            "Monitor surrounding plants"
        ],

        "prevention": [
            "Use clean planting material",
            "Avoid overhead irrigation",
            "Maintain adequate plant spacing",
            "Remove crop debris"
        ],

        "environment": {
            "humidity_threshold": 70,
            "rain_increases_risk": True,
            "temperature_range": (24, 32)
        }
    },


    # =========================================================
    # TOMATO LEAF MOLD
    # =========================================================

    "Tomato___Leaf_Mold": {

        "crop": "Tomato",

        "display_name": "Tomato Leaf Mold",

        "severity": 3,

        "symptoms": [
            "Yellowish spots may appear on the upper leaf surface",
            "Olive-green or brown growth may occur underneath leaves",
            "Older leaves are often affected first",
            "Severely affected leaves may wither"
        ],

        "actions": [
            "Improve ventilation around plants",
            "Reduce excessive humidity where possible",
            "Remove severely affected leaves",
            "Avoid prolonged leaf wetness"
        ],

        "prevention": [
            "Maintain good airflow",
            "Avoid excessive humidity",
            "Space plants appropriately",
            "Remove infected plant debris"
        ],

        "environment": {
            "humidity_threshold": 85,
            "rain_increases_risk": True,
            "temperature_range": (20, 30)
        }
    },


    # =========================================================
    # TOMATO SEPTORIA
    # =========================================================

    "Tomato___Septoria_leaf_spot": {

        "crop": "Tomato",

        "display_name": "Tomato Septoria Leaf Spot",

        "severity": 3,

        "symptoms": [
            "Small circular spots may appear on lower leaves",
            "Spots can have darker borders",
            "Lower leaves are often affected first",
            "Leaves may yellow and drop as the disease progresses"
        ],

        "actions": [
            "Remove severely affected leaves",
            "Improve airflow around the plant",
            "Keep leaves as dry as possible",
            "Monitor disease progression"
        ],

        "prevention": [
            "Remove infected plant debris",
            "Avoid overhead irrigation",
            "Maintain plant spacing",
            "Scout plants regularly"
        ],

        "environment": {
            "humidity_threshold": 70,
            "rain_increases_risk": True,
            "temperature_range": (18, 30)
        }
    },


    # =========================================================
    # POTATO EARLY BLIGHT
    # =========================================================

    "Potato___Early_blight": {

        "crop": "Potato",

        "display_name": "Potato Early Blight",

        "severity": 3,

        "symptoms": [
            "Dark circular spots can occur on older leaves",
            "Concentric ring patterns may develop",
            "Yellowing may occur around lesions",
            "Leaves can dry and fall"
        ],

        "actions": [
            "Remove severely infected foliage",
            "Improve airflow",
            "Keep foliage dry where possible",
            "Monitor surrounding plants"
        ],

        "prevention": [
            "Maintain good crop hygiene",
            "Remove infected debris",
            "Avoid unnecessary leaf wetness",
            "Scout regularly"
        ],

        "environment": {
            "humidity_threshold": 70,
            "rain_increases_risk": True,
            "temperature_range": (20, 30)
        }
    },


    # =========================================================
    # POTATO LATE BLIGHT
    # =========================================================

    "Potato___Late_blight": {

        "crop": "Potato",

        "display_name": "Potato Late Blight",

        "severity": 5,

        "symptoms": [
            "Large dark lesions can develop on leaves",
            "Lesions can spread quickly",
            "White growth can occur in wet conditions",
            "Tubers may also become damaged"
        ],

        "actions": [
            "Inspect the crop immediately",
            "Remove severely affected foliage",
            "Keep foliage as dry as possible",
            "Monitor nearby plants closely"
        ],

        "prevention": [
            "Scout frequently",
            "Avoid prolonged leaf wetness",
            "Maintain adequate spacing",
            "Remove infected plant material"
        ],

        "environment": {
            "humidity_threshold": 75,
            "rain_increases_risk": True,
            "temperature_range": (15, 23)
        }
    },


    # =========================================================
    # PEPPER BACTERIAL SPOT
    # =========================================================

    "Pepper,_bell___Bacterial_spot": {

        "crop": "Bell Pepper",

        "display_name": "Bell Pepper Bacterial Spot",

        "severity": 4,

        "symptoms": [
            "Small brown circular spots can appear on leaves",
            "Dark spots may also appear on fruit",
            "Severe infection can cause leaf damage"
        ],

        "actions": [
            "Remove severely affected leaves",
            "Avoid overhead watering",
            "Avoid handling plants while wet",
            "Improve airflow"
        ],

        "prevention": [
            "Use clean planting material",
            "Maintain plant spacing",
            "Keep foliage dry",
            "Remove crop debris"
        ],

        "environment": {
            "humidity_threshold": 70,
            "rain_increases_risk": True,
            "temperature_range": (24, 32)
        }
    },


    # =========================================================
    # HEALTHY
    # =========================================================

    "Tomato___healthy": {

        "crop": "Tomato",

        "display_name": "Healthy Tomato Leaf",

        "severity": 0,

        "symptoms": [
            "No major disease pattern detected"
        ],

        "actions": [
            "Continue normal crop monitoring",
            "Maintain good growing conditions",
            "Recheck if new symptoms appear"
        ],

        "prevention": [
            "Maintain good airflow",
            "Keep the growing area clean",
            "Scout plants regularly"
        ],

        "environment": {
            "humidity_threshold": 100,
            "rain_increases_risk": False,
            "temperature_range": (0, 50)
        }
    }
}