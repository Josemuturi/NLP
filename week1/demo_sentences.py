"""
week1/demo_sentences.py — Smart Farm Farming Example Sentences (Week 1)
=========================================================================
Five carefully chosen farming sentences that richly demonstrate:
  - Various crop types (maize, tomato, beans, potato, wheat)
  - Action verbs (spray, irrigate, apply, harvest)
  - Descriptive symptoms (yellowing, wilting, rust, blight)
  - Agricultural terminology for NLP processing

These sentences are used by nlp_pipeline.py for Week 1 demonstration.

Course: BIT4133 Natural Language Processing — Week 1
Project: Smart Farm AI Assistant
"""

# =============================================================================
# FIVE FARMING EXAMPLE SENTENCES
# =============================================================================

FARMING_SENTENCES = [
    # Sentence 1: Maize disease symptom
    "My maize leaves are turning yellow and the plants are stunted.",

    # Sentence 2: Tomato pest problem
    "The tomato plants in my field are being attacked by whiteflies and the leaves are curling inward.",

    # Sentence 3: Bean crop action
    "I need to spray my bean crop with fungicide because I can see rust spots forming on the leaves.",

    # Sentence 4: Potato blight concern
    "My potato plants are showing signs of late blight with dark brown lesions spreading quickly across the leaves.",

    # Sentence 5: Wheat water management
    "The wheat field near the river is waterlogged after heavy rains and the plants are beginning to wilt.",
]

# Extended corpus — used by Week 2 N-gram model for training
FARMING_CORPUS = [
    "Maize leaves turn yellow when nitrogen is deficient in the soil.",
    "Apply urea fertilizer to correct nitrogen deficiency in maize.",
    "Tomato blight spreads rapidly in humid and wet weather conditions.",
    "Spray mancozeb fungicide to control late blight in potatoes.",
    "Beans rust appears as orange powdery spots on the leaf surface.",
    "Irrigate the maize field during dry spells to prevent wilting.",
    "Wheat rust is a serious fungal disease that reduces grain yield.",
    "Remove infected tomato plants to prevent disease spread in the field.",
    "Cassava mosaic disease is spread by whiteflies in tropical regions.",
    "Soil testing helps determine the correct fertilizer to apply.",
    "Fall armyworm destroys maize by eating leaves and burrowing into stems.",
    "Plant certified disease-resistant seed varieties to reduce crop losses.",
    "Crop rotation breaks pest and disease cycles in the soil.",
    "The rice blast fungus infects leaves producing diamond-shaped lesions.",
    "Apply compost to improve soil structure and nutrient content.",
    "Phytophthora infestans causes late blight in both potato and tomato crops.",
    "Biological pest control uses natural predators to manage farm pests.",
    "Mulching retains soil moisture and suppresses weed growth on the farm.",
    "Integrated pest management combines chemical cultural and biological methods.",
    "Harvest maize when the grain moisture content is below fourteen percent.",
]

if __name__ == "__main__":
    print("=" * 60)
    print("  Smart Farm — Farming Example Sentences (Week 1 Demo)")
    print("=" * 60)
    print()
    print("FIVE PRIMARY DEMO SENTENCES:")
    print()
    for i, sentence in enumerate(FARMING_SENTENCES, start=1):
        print(f"  {i}. {sentence}")
    print()
    print(f"EXTENDED CORPUS: {len(FARMING_CORPUS)} sentences for N-gram training")
    print()
    for j, sent in enumerate(FARMING_CORPUS, start=1):
        print(f"  {j:2d}. {sent}")
