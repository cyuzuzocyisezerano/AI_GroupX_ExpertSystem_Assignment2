from flask import Flask, render_template_string, request

app = Flask(__name__)

# Database of diseases and remedies
disease_database = {
    'cattle': [
        {
            'id': 1,
            'name': "Bovine Respiratory Disease (BRD)",
            'symptoms': ["coughing", "nasal discharge", "fever", "reduced appetite", "labored breathing"],
            'description': "A complex of diseases affecting the lungs and respiratory tract of cattle.",
            'severity': "High",
            'treatments': [
                {
                    'type': "Medication",
                    'details': "Antibiotics like florfenicol, tulathromycin, or tilmicosin as prescribed by a veterinarian."
                },
                {
                    'type': "Management",
                    'details': "Provide good ventilation, reduce stress, isolate affected animals."
                },
                {
                    'type': "Prevention",
                    'details': "Vaccination against viral pathogens, proper nutrition, and stress management."
                }
            ]
        },
        {
            'id': 2,
            'name': "Foot and Mouth Disease",
            'symptoms': ["fever", "blisters on mouth", "blisters on feet", "excessive salivation", "lameness"],
            'description': "A highly contagious viral disease affecting cloven-hoofed animals.",
            'severity': "Critical - Reportable Disease",
            'treatments': [
                {
                    'type': "Action Required",
                    'details': "Contact veterinary authorities immediately. This is a notifiable disease."
                },
                {
                    'type': "Management",
                    'details': "Quarantine affected animals, implement biosecurity measures."
                },
                {
                    'type': "Treatment",
                    'details': "Supportive care only. Treatment focuses on pain management and preventing secondary infections."
                }
            ]
        },
        {
            'id': 3,
            'name': "Mastitis",
            'symptoms': ["swollen udder", "abnormal milk", "pain in udder", "reduced milk production", "fever"],
            'description': "Inflammation of the mammary gland usually caused by bacterial infection.",
            'severity': "Moderate to High",
            'treatments': [
                {
                    'type': "Medication",
                    'details': "Intramammary antibiotics, systemic antibiotics for severe cases as prescribed by vet."
                },
                {
                    'type': "Supportive Care",
                    'details': "Frequent milking, cold or warm compresses, anti-inflammatory drugs."
                },
                {
                    'type': "Prevention",
                    'details': "Good milking hygiene, proper housing, teat dipping after milking."
                }
            ]
        }
    ],
    'goat': [
        {
            'id': 1,
            'name': "Caprine Arthritis Encephalitis (CAE)",
            'symptoms': ["joint swelling", "lameness", "weight loss", "pneumonia", "neurological symptoms"],
            'description': "A viral disease affecting goats that causes chronic progressive arthritis and encephalitis.",
            'severity': "High - No Cure",
            'treatments': [
                {
                    'type': "Management",
                    'details': "No specific treatment. Manage pain with anti-inflammatory drugs prescribed by a vet."
                },
                {
                    'type': "Prevention",
                    'details': "Testing and culling, separating kids from infected dams at birth."
                },
                {
                    'type': "Supportive Care",
                    'details': "Provide comfortable bedding, easy access to food and water."
                }
            ]
        },
        {
            'id': 2,
            'name': "Enterotoxemia (Overeating Disease)",
            'symptoms': ["sudden death", "abdominal pain", "diarrhea", "convulsions", "bloating"],
            'description': "Caused by Clostridium perfringens bacteria that produce toxins in the intestine.",
            'severity': "Critical",
            'treatments': [
                {
                    'type': "Medication",
                    'details': "Antitoxin, antibiotics, anti-inflammatories as prescribed by vet."
                },
                {
                    'type': "Supportive Care",
                    'details': "Oral electrolytes, IV fluids, reduce feed intake temporarily."
                },
                {
                    'type': "Prevention",
                    'details': "Vaccination, gradual diet changes, avoid overfeeding grain."
                }
            ]
        },
        {
            'id': 3,
            'name': "Coccidiosis",
            'symptoms': ["diarrhea", "weight loss", "dehydration", "weakness", "bloody stool"],
            'description': "A parasitic disease caused by protozoa affecting the intestinal tract.",
            'severity': "Moderate",
            'treatments': [
                {
                    'type': "Medication",
                    'details': "Sulfa drugs, amprolium, or other coccidiostats as prescribed by a vet."
                },
                {
                    'type': "Supportive Care",
                    'details': "Fluids to prevent dehydration, electrolytes, good nutrition."
                },
                {
                    'type': "Prevention",
                    'details': "Clean housing, prevent overcrowding, good sanitation, coccidiostats in feed for prevention."
                }
            ]
        }
    ]
}

# Common symptoms for each animal type
symptoms = {
    'cattle': [
        "coughing", "nasal discharge", "fever", "reduced appetite", "labored breathing", 
        "swollen udder", "abnormal milk", "pain in udder", "reduced milk production",
        "blisters on mouth", "blisters on feet", "excessive salivation", "lameness",
        "diarrhea", "weight loss", "dehydration", "weakness", "bloody stool"
    ],
    'goat': [
        "joint swelling", "lameness", "weight loss", "pneumonia", "neurological symptoms",
        "sudden death", "abdominal pain", "diarrhea", "convulsions", "bloating",
        "dehydration", "weakness", "bloody stool", "fever", "coughing", "reduced appetite"
    ]
}

# Rule-based disease diagnostic system
class LivestockHealthAdvisor:
    def __init__(self):
        self.disease_database = disease_database
        self.symptoms = symptoms
        
    # Rule 1: Filter diseases based on selected symptoms
    def filter_by_symptoms(self, animal_type, selected_symptoms):
        if not selected_symptoms:
            return self.disease_database[animal_type]
            
        filtered_diseases = []
        for disease in self.disease_database[animal_type]:
            # Check if any selected symptom matches the disease
            if any(symptom in disease['symptoms'] for symptom in selected_symptoms):
                filtered_diseases.append(disease)
        
        return filtered_diseases
    
    # Rule 2: Sort diseases by symptom match count (highest first)
    def sort_by_match_count(self, diseases, selected_symptoms):
        if not selected_symptoms:
            return diseases
            
        # Count matching symptoms for each disease and sort
        return sorted(
            diseases,
            key=lambda disease: sum(1 for s in selected_symptoms if s in disease['symptoms']),
            reverse=True
        )
    
    # Rule 3: Filter by search text in name, description, or symptoms
    def filter_by_search_text(self, diseases, search_text):
        if not search_text:
            return diseases
            
        filtered_diseases = []
        search_text = search_text.lower()
        
        for disease in diseases:
            # Check if text is in disease name
            if search_text in disease['name'].lower():
                filtered_diseases.append(disease)
                continue
                
            # Check if text is in description
            if search_text in disease['description'].lower():
                filtered_diseases.append(disease)
                continue
                
            # Check if text is in any symptom
            if any(search_text in symptom for symptom in disease['symptoms']):
                filtered_diseases.append(disease)
                continue
                
        return filtered_diseases
    
    # Rule 4: Identify critical conditions that require immediate veterinary attention
    def flag_critical_conditions(self, diseases):
        for disease in diseases:
            if "Critical" in disease['severity']:
                disease['urgent'] = True
            else:
                disease['urgent'] = False
        return diseases
    
    # Rule 5: Calculate symptom coverage percentage
    def calculate_symptom_coverage(self, diseases, selected_symptoms):
        if not selected_symptoms:
            for disease in diseases:
                disease['symptom_coverage'] = 0
            return diseases
            
        for disease in diseases:
            matching_symptoms = [s for s in selected_symptoms if s in disease['symptoms']]
            disease['matching_symptoms'] = matching_symptoms
            disease['symptom_coverage'] = len(matching_symptoms) / len(selected_symptoms) * 100
            
        return diseases
    
    # Rule 6: Apply severity rating score
    def apply_severity_rating(self, diseases):
        severity_score = {
            "Low": 1,
            "Moderate": 2,
            "Moderate to High": 3,
            "High": 4,
            "Critical": 5,
            "Critical - Reportable Disease": 5
        }
        
        for disease in diseases:
            # Extract base severity without additional text
            base_severity = disease['severity'].split(' - ')[0] if ' - ' in disease['severity'] else disease['severity']
            disease['severity_score'] = severity_score.get(base_severity, 0)
            
        return diseases
    
    # Main search method that applies all rules
    def search_diseases(self, animal_type, selected_symptoms, search_text):
        # Apply rules in sequence
        results = self.filter_by_symptoms(animal_type, selected_symptoms)
        results = self.sort_by_match_count(results, selected_symptoms)
        results = self.filter_by_search_text(results, search_text)
        results = self.flag_critical_conditions(results)
        results = self.calculate_symptom_coverage(results, selected_symptoms)
        results = self.apply_severity_rating(results)
        
        return results

# Initialize our health advisor
health_advisor = LivestockHealthAdvisor()

# HTML Templates as strings

# Index template
INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Livestock Health Advisor</title>
    <style>
        /* You can add your CSS styles here */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            text-align: center;
            margin-bottom: 30px;
        }
        .subtitle {
            font-size: 1.2em;
            color: #666;
        }
        .animal-selector {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        .animal-type {
            cursor: pointer;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            text-align: center;
        }
        .animal-type img {
            max-width: 100px;
            height: auto;
        }
        .active {
            border-color: #007bff;
            background-color: #f0f7ff;
        }
        .search-section {
            margin-bottom: 30px;
        }
        .search-box {
            display: flex;
            margin-bottom: 20px;
        }
        .search-box input {
            flex-grow: 1;
            padding: 10px;
            font-size: 1em;
        }
        .search-box button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
        .symptoms-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
        }
        .symptom-checkbox {
            display: flex;
            align-items: center;
        }
        .emergency-banner {
            background-color: #ffebee;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
        .disease-card {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .disease-name {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .severity {
            background-color: #f8d7da;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            margin-left: 10px;
        }
        .disease-details {
            display: flex;
            margin-top: 15px;
        }
        .disease-image {
            flex: 0 0 150px;
            margin-right: 15px;
        }
        .disease-image img {
            max-width: 100%;
            height: auto;
        }
        .disease-info {
            flex-grow: 1;
        }
        .treatment-section {
            margin-top: 10px;
        }
        .treatment-option {
            margin-bottom: 10px;
        }
        footer {
            margin-top: 30px;
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Livestock Health Advisor</h1>
            <div class="subtitle">Expert Remedies for Goats & Cattle</div>
        </header>
        
        <div class="main-content">
            <form action="/search" method="post" class="search-section">
                <div class="animal-selector">
                    <div class="animal-type {% if animal_type == 'cattle' or not animal_type %}active{% endif %}" id="cattle-selector">
                        <img src="/static/images/livestock-1822698_1280.jpg" alt="Cattle">
                        <span>Cattle</span>
                        <input type="radio" name="animal_type" value="cattle" {% if animal_type == 'cattle' or not animal_type %}checked{% endif %} style="display: none;">
                    </div>
                    <div class="animal-type {% if animal_type == 'goat' %}active{% endif %}" id="goat-selector">
                        <img src="/static/images/irish-goat-7429437_1280.jpg" alt="Goat">
                        <span>Goat</span>
                        <input type="radio" name="animal_type" value="goat" {% if animal_type == 'goat' %}checked{% endif %} style="display: none;">
                    </div>
                </div>
                
                <div class="search-box">
                    <input type="text" id="search-input" name="search_text" placeholder="Search symptoms or diseases...">
                    <button type="submit">Find Remedies</button>
                </div>
                
                <div>
                    <h3>Select Symptoms:</h3>
                    <div class="symptoms-container" id="cattle-symptoms" {% if animal_type == 'goat' %}style="display: none;"{% endif %}>
                        {% for symptom in cattle_symptoms %}
                        <div class="symptom-checkbox">
                            <input type="checkbox" id="cattle-{{ symptom }}" name="symptoms" value="{{ symptom }}">
                            <label for="cattle-{{ symptom }}">{{ symptom[0]|upper }}{{ symptom[1:] }}</label>
                        </div>
                        {% endfor %}
                    </div>
                    
                    <div class="symptoms-container" id="goat-symptoms" {% if animal_type != 'goat' %}style="display: none;"{% endif %}>
                        {% for symptom in goat_symptoms %}
                        <div class="symptom-checkbox">
                            <input type="checkbox" id="goat-{{ symptom }}" name="symptoms" value="{{ symptom }}">
                            <label for="goat-{{ symptom }}">{{ symptom[0]|upper }}{{ symptom[1:] }}</label>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </form>
            
            <div class="emergency-banner">
                <strong>Important:</strong> In case of severe symptoms or emergency, contact a veterinarian immediately.
            </div>
        </div>
        
        <footer>
            <p>This tool provides general information only. Always consult with a qualified veterinarian for diagnosis and treatment.</p>
            <p>&copy; 2025 Livestock Health Advisor</p>
        </footer>
    </div>
    
    <script>
        // Simple JavaScript to toggle between animal types
        document.getElementById('cattle-selector').addEventListener('click', function() {
            document.querySelector('input[value="cattle"]').checked = true;
            document.getElementById('cattle-selector').classList.add('active');
            document.getElementById('goat-selector').classList.remove('active');
            document.getElementById('cattle-symptoms').style.display = 'grid';
            document.getElementById('goat-symptoms').style.display = 'none';
        });
        
        document.getElementById('goat-selector').addEventListener('click', function() {
            document.querySelector('input[value="goat"]').checked = true;
            document.getElementById('goat-selector').classList.add('active');
            document.getElementById('cattle-selector').classList.remove('active');
            document.getElementById('goat-symptoms').style.display = 'grid';
            document.getElementById('cattle-symptoms').style.display = 'none';
        });
    </script>
</body>
</html>
'''

# Results template
RESULTS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Livestock Health Advisor - Results</title>
    <style>
        /* You can add your CSS styles here - same as index.html */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            text-align: center;
            margin-bottom: 30px;
        }
        .subtitle {
            font-size: 1.2em;
            color: #666;
        }
        .emergency-banner {
            background-color: #ffebee;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
        .result-section {
            margin-bottom: 30px;
        }
        .disease-card {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .disease-name {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .severity {
            background-color: #f8d7da;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            margin-left: 10px;
        }
        .critical {
            background-color: #dc3545;
            color: white;
        }
        .high {
            background-color: #f8d7da;
        }
        .moderate {
            background-color: #fff3cd;
        }
        .low {
            background-color: #d1e7dd;
        }
        .disease-details {
            display: flex;
            margin-top: 15px;
        }
        .disease-image {
            flex: 0 0 150px;
            margin-right: 15px;
        }
        .disease-image img {
            max-width: 100%;
            height: auto;
        }
        .disease-info {
            flex-grow: 1;
        }
        .treatment-section {
            margin-top: 10px;
        }
        .treatment-option {
            margin-bottom: 10px;
        }
        .back-button {
            display: inline-block;
            margin-bottom: 20px;
            padding: 10px 20px;
            background-color: #6c757d;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .symptom-coverage {
            margin-top: 10px;
            font-style: italic;
        }
        .matching-symptoms {
            background-color: #e2f0d9;
            padding: 5px;
            border-radius: 3px;
        }
        footer {
            margin-top: 30px;
            text-align: center;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Livestock Health Advisor</h1>
            <div class="subtitle">Expert Remedies for Goats & Cattle</div>
        </header>
        
        <a href="/" class="back-button">« Back to Search</a>
        
        <div class="main-content">
            <div class="emergency-banner">
                <strong>Important:</strong> In case of severe symptoms or emergency, contact a veterinarian immediately.
            </div>
            
            <div class="result-section">
                <h2>Possible Conditions for {{ animal_type|capitalize }}:</h2>
                
                {% if selected_symptoms %}
                <p>
                    <strong>Selected symptoms:</strong> 
                    {% for symptom in selected_symptoms %}
                        <span class="matching-symptoms">{{ symptom[0]|upper }}{{ symptom[1:] }}</span>{% if not loop.last %}, {% endif %}
                    {% endfor %}
                </p>
                {% endif %}
                
                <div id="disease-results">
                    {% if results|length == 0 %}
                        <p>No matching conditions found. Try selecting different symptoms or consult a veterinarian.</p>
                    {% else %}
                        {% for disease in results %}
                            <div class="disease-card">
                                <div class="disease-name">
                                    {{ disease.name }} 
                                    <span class="severity {% if disease.severity_score >= 5 %}critical{% elif disease.severity_score >= 4 %}high{% elif disease.severity_score >= 2 %}moderate{% else %}low{% endif %}">
                                        {{ disease.severity }}
                                    </span>
                                    {% if disease.urgent %}
                                        <span style="color: red; font-weight: bold; margin-left: 10px;">URGENT: CONTACT VET IMMEDIATELY</span>
                                    {% endif %}
                                </div>
                                
                                <p>{{ disease.description }}</p>
                                
                                <p><strong>Symptoms:</strong> 
                                    {% for symptom in disease.symptoms %}
                                        {% if selected_symptoms and symptom in selected_symptoms %}
                                            <span class="matching-symptoms">{{ symptom[0]|upper }}{{ symptom[1:] }}</span>
                                        {% else %}
                                            {{ symptom[0]|upper }}{{ symptom[1:] }}
                                        {% endif %}
                                        {% if not loop.last %}, {% endif %}
                                    {% endfor %}
                                </p>
                                
                                {% if selected_symptoms and disease.matching_symptoms %}
                                    <p class="symptom-coverage">
                                        <strong>Symptom match:</strong> {{ disease.symptom_coverage|round(1) }}% ({{ disease.matching_symptoms|length }} of {{ selected_symptoms|length }} symptoms)
                                    </p>
                                {% endif %}
                                
                                <div class="disease-details">
                                    <div class="disease-image">
                                        <img src="/static/images/shutterstock_1571593363-scaled.jpg" alt="{{ disease.name }}">
                                    </div>
                                    <div class="disease-info">
                                        <div class="treatment-section">
                                            <h3>Recommended Treatments:</h3>
                                            {% for treatment in disease.treatments %}
                                                <div class="treatment-option">
                                                    <h4>{{ treatment.type }}</h4>
                                                    <p>{{ treatment.details }}</p>
                                                </div>
                                            {% endfor %}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    {% endif %}
                </div>
            </div>
        </div>
        
        <footer>
            <p>This tool provides general information only. Always consult with a qualified veterinarian for diagnosis and treatment.</p>
            <p>&copy; 2025 Livestock Health Advisor</p>
        </footer>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(
        INDEX_TEMPLATE, 
        cattle_symptoms=symptoms['cattle'], 
        goat_symptoms=symptoms['goat'],
        animal_type='cattle'
    )

@app.route('/search', methods=['POST'])
def search():
    # Get data from the form
    animal_type = request.form.get('animal_type', 'cattle')
    search_text = request.form.get('search_text', '')
    selected_symptoms = request.form.getlist('symptoms')
    
    # Apply our rule-based system
    results = health_advisor.search_diseases(animal_type, selected_symptoms, search_text)
    
    return render_template_string(
        RESULTS_TEMPLATE, 
        results=results, 
        animal_type=animal_type, 
        selected_symptoms=selected_symptoms
    )

# For serving static files in development (would need proper setup for production)
@app.route('/static/images/<path:filename>')
def serve_image(filename):
    from flask import send_from_directory
    import os
    # This is only for demo purposes - you'd need to set up proper static file serving for production
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), filename)

if __name__ == '__main__':
    import os
    # Create static/images directory if it doesn't exist
    if not os.path.exists(os.path.join(app.root_path, 'static', 'images')):
        os.makedirs(os.path.join(app.root_path, 'static', 'images'))
    
    app.run(debug=True)