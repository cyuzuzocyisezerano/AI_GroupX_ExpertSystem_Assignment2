# Simple Animal Disease Remedies Suggestion System

# Dictionary of common diseases and their remedies
disease_remedies = {
    # Cattle diseases
    "bovine respiratory disease": [
        "Consult a veterinarian for appropriate antibiotics",
        "Provide good ventilation in housing",
        "Isolate affected animals",
        "Ensure adequate nutrition and hydration"
    ],
    "mastitis": [
        "Consult a veterinarian for appropriate antibiotics",
        "Regular milking of affected quarters",
        "Apply warm compresses to udder",
        "Maintain clean bedding and milking equipment"
    ],
    "foot rot": [
        "Clean and trim hooves",
        "Apply topical antibiotics or copper sulfate",
        "Keep affected animals in dry areas",
        "Footbaths with zinc or copper sulfate solution"
    ],
    
    # Goat diseases
    "caprine arthritis encephalitis": [
        "No cure - manage symptoms",
        "Provide soft bedding and easy access to food/water",
        "Anti-inflammatory medications (prescribed by vet)",
        "Separate infected animals to prevent spread"
    ],
    "coccidiosis": [
        "Administer anticoccidial medications (consult vet)",
        "Improve sanitation in living areas",
        "Ensure proper nutrition",
        "Reduce overcrowding"
    ],
    "enterotoxemia": [
        "Vaccination for prevention",
        "Antitoxin for acute cases (vet prescribed)",
        "Gradual diet changes",
        "Limit grain intake"
    ],
    
    # General diseases affecting multiple species
    "parasites": [
        "Appropriate deworming medication (consult vet)",
        "Rotate pastures if possible",
        "Regular fecal testing",
        "Maintain clean living environment"
    ],
    "bloat": [
        "For mild cases: walking the animal",
        "Stomach tube to relieve pressure (by professional)",
        "Anti-bloating medication",
        "Dietary management to prevent recurrence"
    ]
}

def suggest_remedies(animal_type, symptoms):
    """
    Suggest potential remedies based on animal type and symptoms
    
    Parameters:
    animal_type (str): Type of animal (cattle, goat, etc.)
    symptoms (list): List of symptoms the animal is showing
    
    Returns:
    dict: Possible diseases and their remedies
    """
    possible_diseases = {}
    
    # Simple keyword matching for demonstration
    keyword_to_disease = {
        "coughing": ["bovine respiratory disease"],
        "nasal discharge": ["bovine respiratory disease"],
        "udder swelling": ["mastitis"],
        "abnormal milk": ["mastitis"],
        "lameness": ["foot rot", "caprine arthritis encephalitis"],
        "joint swelling": ["caprine arthritis encephalitis"],
        "diarrhea": ["coccidiosis", "enterotoxemia", "parasites"],
        "weight loss": ["parasites", "caprine arthritis encephalitis"],
        "bloating": ["bloat", "enterotoxemia"]
    }
    
    # Match symptoms to diseases
    for symptom in symptoms:
        if symptom.lower() in keyword_to_disease:
            for disease in keyword_to_disease[symptom.lower()]:
                if animal_type.lower() == "cattle" and disease in ["caprine arthritis encephalitis"]:
                    continue  # Skip goat-specific diseases for cattle
                if animal_type.lower() == "goat" and disease in ["bovine respiratory disease"]:
                    continue  # Skip cattle-specific diseases for goats
                    
                if disease in disease_remedies:
                    possible_diseases[disease] = disease_remedies[disease]
    
    return possible_diseases

# Example usage
if __name__ == "__main__":
    print("=== Livestock Health Advisor ===")
    
    animal_type = input("Enter animal type (cattle/goat): ").strip()
    symptoms_input = input("Enter symptoms (comma separated): ").strip()
    
    symptoms = [s.strip() for s in symptoms_input.split(',')]
    
    results = suggest_remedies(animal_type, symptoms)
    
    if results:
        print("\nPossible conditions and remedies:")
        for disease, remedies in results.items():
            print(f"\n{disease.upper()}:")
            for i, remedy in enumerate(remedies, 1):
                print(f"  {i}. {remedy}")
    else:
        print("\nNo specific remedies found for these symptoms.")
        print("Please consult a veterinarian for proper diagnosis and treatment.")
        
    print("\nDisclaimer: This is a basic advisory tool. Always consult a qualified veterinarian for diagnosis and treatment.")
