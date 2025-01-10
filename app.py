from flask import Flask, request, jsonify
import joblib

# Load the saved KNN model
model = joblib.load('knn_model.pkl')

# Initialize Flask app
app = Flask(__name__)

# Function to classify season
def classify_season(temp, rainfall):
    if temp >= 25 and rainfall >= 200:
        return 'Monsoon'
    elif temp < 20 and rainfall < 50:
        return 'Winter'
    else:
        return 'Summer'

# Function to classify soil type
def classify_soil_type(ph):
    if ph < 6:
        return 'Acidic'
    elif 6 <= ph <= 7:
        return 'Neutral'
    else:
        return 'Alkaline'

# Define a route for predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the request
    data = request.get_json()

    # Extract features
    temperature = data['temperature']
    rainfall = data['rainfall']
    ph = data['ph']
    N = data['N']
    P = data['P']
    K = data['K']

    # Create derived features
    season = classify_season(temperature, rainfall)
    soil_type = classify_soil_type(ph)
    N_P_ratio = N / (P + 1e-6)
    K_Temp_ratio = K / (temperature + 1e-6)

    # Prepare the feature list for prediction
    features = [
        N, P, K, temperature, data['humidity'], ph, rainfall,
        N_P_ratio, K_Temp_ratio,
        int(season == 'Monsoon'), int(season == 'Summer'), int(season == 'Winter'),
        int(soil_type == 'Acidic'), int(soil_type == 'Alkaline'), int(soil_type == 'Neutral')
    ]

    # Make prediction
    prediction = model.predict([features])

    # Return the prediction as JSON
    return jsonify({'prediction': int(prediction[0])})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
