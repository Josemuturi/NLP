"""
knowledge_base.py — Smart Farm Knowledge Base
===============================================
A structured dictionary mapping farming problems (crop + symptom/condition)
to practical solutions. Used by the chatbot to return answers to farmer queries.

Course: BIT4133 Natural Language Processing
Project: Smart Farm AI Assistant
"""

# =============================================================================
# FARMING KNOWLEDGE BASE
# Keys: tuples of (crop, symptom/issue) — both lowercase
# Values: dict with 'cause', 'solution', and 'action' fields
# =============================================================================

KNOWLEDGE_BASE = {

    # ── MAIZE ──────────────────────────────────────────────────────────────
    ("maize", "yellow leaves"): {
        "cause": "Nitrogen deficiency or Maize Streak Virus (MSV).",
        "solution": "Apply urea fertilizer (46% N) at 50 kg/acre. If viral symptoms "
                    "(yellow streaks), remove and destroy infected plants, control aphid vectors.",
        "action": "fertilize | remove infected plants",
        "severity": "medium"
    },
    ("maize", "stunted growth"): {
        "cause": "Poor soil fertility, waterlogging, or fall armyworm infestation.",
        "solution": "Conduct soil test and apply NPK 23:23:0 basal fertilizer. Ensure "
                    "proper drainage. Spray with emamectin benzoate for armyworm control.",
        "action": "soil test | drain field | spray insecticide",
        "severity": "high"
    },
    ("maize", "brown spots"): {
        "cause": "Northern Leaf Blight (Turcicum leaf blight) caused by fungus Exserohilum turcicum.",
        "solution": "Spray mancozeb or propiconazole fungicide. Rotate crops and use resistant varieties.",
        "action": "spray fungicide | crop rotation",
        "severity": "medium"
    },
    ("maize", "wilting"): {
        "cause": "Drought stress or Fusarium stalk rot.",
        "solution": "Irrigate immediately if drought. For stalk rot, improve drainage and "
                    "avoid mechanical injuries. Plant resistant varieties next season.",
        "action": "irrigate | improve drainage",
        "severity": "high"
    },
    ("maize", "pests"): {
        "cause": "Fall armyworm (Spodoptera frugiperda) or stem borers.",
        "solution": "Apply chlorpyrifos or spinosad insecticide. Use push-pull companion "
                    "planting with Desmodium and Napier grass borders.",
        "action": "spray insecticide | companion planting",
        "severity": "high"
    },

    # ── TOMATO ─────────────────────────────────────────────────────────────
    ("tomato", "yellow leaves"): {
        "cause": "Magnesium deficiency, early blight, or Tomato Yellow Leaf Curl Virus (TYLCV).",
        "solution": "Spray Epsom salt solution (magnesium sulphate) for deficiency. "
                    "For early blight, apply copper-based fungicide. For TYLCV, control whiteflies.",
        "action": "spray fungicide | control whiteflies | foliar feed",
        "severity": "medium"
    },
    ("tomato", "blight"): {
        "cause": "Early blight (Alternaria solani) or late blight (Phytophthora infestans).",
        "solution": "Remove infected leaves immediately. Spray mancozeb for early blight "
                    "or metalaxyl for late blight. Avoid overhead irrigation.",
        "action": "remove infected parts | spray fungicide",
        "severity": "high"
    },
    ("tomato", "wilting"): {
        "cause": "Fusarium or Verticillium wilt (soilborne fungi) or bacterial wilt.",
        "solution": "There is no cure once infected. Remove and destroy plants. "
                    "Solarize soil, rotate with non-solanaceous crops for 3 seasons.",
        "action": "remove plants | soil solarization | crop rotation",
        "severity": "high"
    },
    ("tomato", "cracking"): {
        "cause": "Irregular watering causing rapid fruit expansion.",
        "solution": "Maintain consistent irrigation schedule. Apply mulch to retain soil moisture.",
        "action": "regulate irrigation | mulch",
        "severity": "low"
    },
    ("tomato", "pests"): {
        "cause": "Aphids, whiteflies, or tomato fruit borer (Helicoverpa armigera).",
        "solution": "Spray imidacloprid for whiteflies/aphids. Use pheromone traps for "
                    "fruit borer. Introduce ladybird beetles as biological control.",
        "action": "spray insecticide | pheromone traps | biocontrol",
        "severity": "medium"
    },

    # ── BEANS ──────────────────────────────────────────────────────────────
    ("beans", "yellow leaves"): {
        "cause": "Iron or nitrogen deficiency, or Bean Common Mosaic Virus (BCMV).",
        "solution": "Apply foliar fertilizer with micronutrients. For BCMV, use certified "
                    "virus-free seed and control aphid vectors with insecticide.",
        "action": "foliar feed | use certified seed | control aphids",
        "severity": "medium"
    },
    ("beans", "rust"): {
        "cause": "Bean rust caused by fungus Uromyces appendiculatus.",
        "solution": "Spray propiconazole or mancozeb fungicide every 10–14 days. "
                    "Plant resistant varieties. Remove crop debris after harvest.",
        "action": "spray fungicide | remove debris",
        "severity": "medium"
    },
    ("beans", "poor germination"): {
        "cause": "Low soil temperature, poor seed quality, or seed rot.",
        "solution": "Use certified seeds. Treat seeds with fungicide (thiram) before planting. "
                    "Plant when soil temperature is above 15°C.",
        "action": "seed treatment | check soil temperature",
        "severity": "medium"
    },
    ("beans", "pests"): {
        "cause": "Bean fly, aphids, or bean weevil in storage.",
        "solution": "Treat seeds with insecticide before planting. Spray dimethoate "
                    "for bean fly. Store harvested beans with ash or diatomite.",
        "action": "spray insecticide | proper storage",
        "severity": "medium"
    },

    # ── WHEAT ──────────────────────────────────────────────────────────────
    ("wheat", "rust"): {
        "cause": "Wheat stem rust (Puccinia graminis) or yellow rust (P. striiformis).",
        "solution": "Spray tebuconazole or propiconazole fungicide at first sign. "
                    "Use resistant varieties (e.g., Kenya Fahari). Plant at recommended time.",
        "action": "spray fungicide | use resistant variety",
        "severity": "high"
    },
    ("wheat", "yellow leaves"): {
        "cause": "Yellow rust infection or sulphur deficiency.",
        "solution": "Apply sulphur-containing fertilizer. Spray fungicide if rust is confirmed.",
        "action": "apply fertilizer | spray fungicide",
        "severity": "medium"
    },
    ("wheat", "lodging"): {
        "cause": "Excessive nitrogen, weak stem varieties, or heavy rainfall.",
        "solution": "Reduce nitrogen application. Use short-stemmed varieties. "
                    "Apply growth regulators (chlormequat) if available.",
        "action": "reduce fertilizer | use short varieties",
        "severity": "medium"
    },

    # ── POTATO ─────────────────────────────────────────────────────────────
    ("potato", "blight"): {
        "cause": "Late blight caused by Phytophthora infestans (most destructive potato disease).",
        "solution": "Begin preventive spraying with mancozeb before symptoms appear. "
                    "Switch to metalaxyl+mancozeb when blight is confirmed. "
                    "Destroy all infected plant material. Use certified seed potatoes.",
        "action": "spray fungicide | destroy infected material | use certified seed",
        "severity": "critical"
    },
    ("potato", "yellow leaves"): {
        "cause": "Early blight, nutrient deficiency, or Potato Virus Y (PVY).",
        "solution": "Apply foliar nitrogen. Spray mancozeb for early blight. "
                    "For PVY, use virus-tested seed and control aphids.",
        "action": "foliar feed | spray fungicide | control aphids",
        "severity": "medium"
    },
    ("potato", "wilting"): {
        "cause": "Bacterial wilt (Ralstonia solanacearum) or drought.",
        "solution": "For bacterial wilt: no chemical cure — remove and burn infected plants, "
                    "rotate with non-solanaceous crops for 4 years. "
                    "For drought: irrigate regularly.",
        "action": "remove plants | crop rotation | irrigate",
        "severity": "high"
    },

    # ── RICE ───────────────────────────────────────────────────────────────
    ("rice", "blast"): {
        "cause": "Rice blast caused by fungus Magnaporthe oryzae.",
        "solution": "Spray tricyclazole or isoprothiolane fungicide. Use resistant varieties. "
                    "Avoid excessive nitrogen. Drain fields periodically.",
        "action": "spray fungicide | use resistant variety | reduce nitrogen",
        "severity": "high"
    },
    ("rice", "yellow leaves"): {
        "cause": "Iron toxicity, nitrogen deficiency, or rice yellow mottle virus.",
        "solution": "For iron toxicity, improve drainage. Apply split doses of nitrogen. "
                    "For viral disease, control insect vectors and use resistant varieties.",
        "action": "improve drainage | split nitrogen application",
        "severity": "medium"
    },
    ("rice", "pests"): {
        "cause": "Stem borers or brown plant hopper (BPH).",
        "solution": "Apply carbofuran granules for stem borers. Spray buprofezin for BPH. "
                    "Avoid excessive nitrogen which attracts BPH.",
        "action": "apply insecticide | reduce nitrogen",
        "severity": "high"
    },

    # ── CASSAVA ────────────────────────────────────────────────────────────
    ("cassava", "mosaic"): {
        "cause": "Cassava Mosaic Disease (CMD) caused by cassava mosaic virus, spread by whiteflies.",
        "solution": "Use CMD-resistant varieties (e.g., NASE 14). Remove infected plants. "
                    "Source clean planting material from certified nurseries.",
        "action": "use resistant variety | remove infected plants | clean planting material",
        "severity": "high"
    },
    ("cassava", "brown streak"): {
        "cause": "Cassava Brown Streak Disease (CBSD) caused by virus, whitefly-transmitted.",
        "solution": "Use CBSD-resistant or tolerant varieties. Obtain virus-tested cuttings. "
                    "Control whitefly populations with insecticide.",
        "action": "use resistant variety | control whiteflies",
        "severity": "critical"
    },
    ("cassava", "root rot"): {
        "cause": "Phytophthora root rot due to waterlogged soils.",
        "solution": "Improve drainage by mounding or ridging. Avoid planting in flood-prone areas. "
                    "Apply appropriate fungicide to planting material.",
        "action": "improve drainage | mound planting",
        "severity": "high"
    },

    # ── GENERAL / FALLBACK ─────────────────────────────────────────────────
    ("general", "pests"): {
        "cause": "Various insect pests common to many crops.",
        "solution": "Identify the specific pest first. Use Integrated Pest Management (IPM): "
                    "biological controls, cultural practices, and chemical sprays only as last resort. "
                    "Consult your local agricultural extension officer.",
        "action": "identify pest | IPM approach | consult extension officer",
        "severity": "varies"
    },
    ("general", "soil"): {
        "cause": "Poor soil health: low pH, nutrient deficiency, or poor structure.",
        "solution": "Conduct a soil test. Lime acid soils (pH < 5.5). Apply balanced NPK fertilizer. "
                    "Add organic matter (compost or farmyard manure) to improve soil structure.",
        "action": "soil test | lime | fertilize | add compost",
        "severity": "medium"
    },
    ("general", "water"): {
        "cause": "Drought stress or waterlogging.",
        "solution": "For drought: irrigate, mulch, and use drought-tolerant varieties. "
                    "For waterlogging: improve drainage with furrows or raised beds.",
        "action": "irrigate | mulch | improve drainage",
        "severity": "high"
    },
}

# =============================================================================
# ENTITY VOCABULARY — used by HMM and keyword matching
# =============================================================================

CROP_VOCAB = [
    "maize", "corn", "tomato", "tomatoes", "bean", "beans", "wheat",
    "potato", "potatoes", "rice", "cassava", "sorghum", "millet",
    "cabbage", "kale", "sukuma", "onion", "onions", "carrot", "carrots",
    "mango", "banana", "coffee", "tea", "sunflower", "groundnut", "peanut"
]

SYMPTOM_VOCAB = [
    "yellow", "yellowing", "brown", "browning", "wilting", "wilt",
    "spots", "spot", "rust", "blight", "mosaic", "stunted", "dying",
    "rotting", "rot", "cracking", "crack", "drooping", "pale", "dry",
    "black", "dead", "weak", "lodging"
]

DISEASE_VOCAB = [
    "blight", "rust", "mosaic", "wilt", "streak", "rot", "blast",
    "mildew", "smut", "virus", "fungus", "bacterial", "armyworm",
    "stemborer", "aphid", "whitefly", "weevil"
]

ACTION_VOCAB = [
    "spray", "apply", "water", "irrigate", "fertilize", "plant",
    "remove", "harvest", "treat", "control", "prune", "drain",
    "mulch", "rotate", "test"
]

LOCATION_VOCAB = [
    "leaves", "leaf", "stem", "root", "roots", "fruit", "fruits",
    "seeds", "seed", "field", "farm", "soil", "stalk", "flower",
    "branch", "trunk", "bark"
]


def lookup_solution(crop: str, symptom: str) -> dict:
    """
    Look up a farming solution from the knowledge base.

    Args:
        crop (str): The crop name (e.g., 'maize')
        symptom (str): The symptom or problem (e.g., 'yellow leaves')

    Returns:
        dict: Solution dictionary with cause, solution, action, severity.
              Returns a fallback response if no exact match found.
    """
    # Normalize inputs
    crop = crop.lower().strip()
    symptom = symptom.lower().strip()

    # Direct match
    if (crop, symptom) in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[(crop, symptom)]

    # Partial symptom match — try each key where the crop matches
    for (kb_crop, kb_symptom), info in KNOWLEDGE_BASE.items():
        if kb_crop == crop and any(word in symptom for word in kb_symptom.split()):
            return info

    # Symptom-only match (general crop)
    for (kb_crop, kb_symptom), info in KNOWLEDGE_BASE.items():
        if kb_crop == "general" and any(word in symptom for word in kb_symptom.split()):
            return info

    # Ultimate fallback
    return {
        "cause": "The specific problem could not be identified from the description.",
        "solution": (
            f"For issues with {crop if crop != 'general' else 'your crop'}, consult your local "
            "agricultural extension officer. Describe the symptoms clearly: which plant part is "
            "affected, color changes, and whether the problem is spreading."
        ),
        "action": "consult extension officer | observe symptoms",
        "severity": "unknown"
    }


def get_all_problems() -> list:
    """Return a list of all (crop, symptom) pairs in the knowledge base."""
    return [(crop, symptom) for (crop, symptom) in KNOWLEDGE_BASE.keys()
            if crop != "general"]


if __name__ == "__main__":
    # Quick test
    print("=== Knowledge Base Test ===")
    result = lookup_solution("maize", "yellow leaves")
    print(f"Crop: maize | Symptom: yellow leaves")
    print(f"Cause   : {result['cause']}")
    print(f"Solution: {result['solution']}")
    print(f"Action  : {result['action']}")
    print(f"Severity: {result['severity']}")
    print()
    print(f"Total entries in knowledge base: {len(KNOWLEDGE_BASE)}")
