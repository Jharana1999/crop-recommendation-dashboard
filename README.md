# Intelligent Crop Recommendation System using Soil and Weather Conditions

## Project Overview
This project implements a complete machine learning pipeline to recommend the most suitable crop for a given set of soil and weather conditions. The aim is to ensure higher yield and optimal resource usage. The system involves data preprocessing, exploratory data analysis, machine learning model development, and deployment through Flask and Dash frameworks.

## Features
1. **Data Exploration and Preprocessing**
   - Handling outliers in temperature and rainfall.
   - Seasonal and soil type classification.
   - Feature scaling and interaction feature creation.
   - Encoding categorical data.

2. **Machine Learning**
   - Training KNN and Logistic Regression models.
   - Hyperparameter tuning using GridSearchCV.
   - Evaluation metrics including accuracy, precision, recall, and F1-score.

3. **Model Deployment**
   - A Flask API to handle predictions.
   - A Dash-based interactive dashboard for user inputs and visualizations.

4. **Visualization**
   - Count plots, histograms, pair plots, and scatter plots to explore the data and results.

## Dataset
The dataset is sourced from Kaggle and contains the following fields:
- **N, P, K**: Soil nutrients (Nitrogen, Phosphorus, Potassium).
- **temperature**: Temperature of the location.
- **humidity**: Humidity percentage.
- **ph**: pH value of the soil.
- **rainfall**: Rainfall in mm.
- **label**: Crop type (target variable).

## Dependencies
Install the following libraries before running the project:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn flask dash plotly joblib dash-bootstrap-components
```

## Directory Structure
```
├── crop_recommendation.csv         # Dataset
├── knn_model.pkl                   # Saved KNN model
├── app.py                          # Flask API for predictions
├── dashboard.py                    # Dash-based interactive dashboard
├── README.md                       # Project documentation
```

## Instructions
### 1. Data Preprocessing
The dataset is preprocessed using:
- Outlier detection and clipping.
- Feature engineering for seasonal and soil type classification.
- Scaling numerical features using MinMaxScaler.
- Encoding categorical variables.

### 2. Model Training
- Train and evaluate a KNN model with hyperparameter tuning.
- Train a Logistic Regression model for comparison.
- Save the best KNN model to a file (`knn_model.pkl`).

### 3. Running the Flask API
To start the Flask API for predictions:
```bash
python app.py
```
The API runs at `http://127.0.0.1:5000`.

#### Example Request to the Flask API:
```json
POST /predict
{
  "N": 50,
  "P": 40,
  "K": 30,
  "temperature": 25.0,
  "humidity": 80.0,
  "ph": 6.5,
  "rainfall": 200.0
}
```
#### Example Response:
```json
{
  "prediction": 20
}
```

### 4. Running the Dashboard
To launch the interactive dashboard:
```bash
python dashboard.py
```
Access the dashboard at `http://127.0.0.1:8050`.

#### Dashboard Features:
- Input fields for nutrient levels, temperature, humidity, pH, and rainfall.
- Predict the recommended crop based on the inputs.
- Scatter plot visualization with customizable X and Y axes.

## Results
- **KNN Model**:
  - Training Accuracy: 99.2%
  - Test Accuracy: 97.3%
- **Logistic Regression Model**:
  - Training Accuracy: 94.4%
  - Test Accuracy: 92.3%

## Future Work
- Incorporate real-time weather data from APIs.
- Extend the model to recommend fertilizers and irrigation strategies.
- Optimize the deployment to cloud services for scalability.

## License
This project is for educational purposes. Please refer to the Kaggle dataset's license for data usage terms.

---
For any issues or queries, feel free to reach out!


