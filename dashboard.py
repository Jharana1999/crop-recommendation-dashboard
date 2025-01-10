import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import requests
import plotly.express as px
import pandas as pd

# Load your dataset
df = pd.read_csv(r'C:\Users\jhara\Desktop\Projects\Datasets\crop_recommendation.csv')

# Define the crop mapping (use the same mapping from your Flask API)
crop_mapping = {
    0: 'Apple', 1: 'Banana', 2: 'Blackgram', 3: 'Chickpea', 4: 'Coconut', 5: 'Coffee',
    6: 'Cotton', 7: 'Grapes', 8: 'Jute', 9: 'Kidney Beans', 10: 'Lentil', 11: 'Maize',
    12: 'Mango', 13: 'Moth Beans', 14: 'Mung Bean', 15: 'Muskmelon', 16: 'Orange',
    17: 'Papaya', 18: 'Pigeon Peas', 19: 'Pomegranate', 20: 'Rice', 21: 'Watermelon'
}

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Crop Recommendation Dashboard", className="text-center text-primary mb-4"), width=12)
    ]),

    # Input fields for prediction
    dbc.Row([
        dbc.Col([
            html.H2("Predict the Best Crop", className="text-center"),
            dcc.Input(id='input-N', type='number', placeholder='Enter Nitrogen (N)', className="mb-2"),
            dcc.Input(id='input-P', type='number', placeholder='Enter Phosphorus (P)', className="mb-2 mx-2"),
            dcc.Input(id='input-K', type='number', placeholder='Enter Potassium (K)', className="mb-2 mx-2"),
            dcc.Input(id='input-temperature', type='number', placeholder='Enter Temperature', className="mb-2 mx-2"),
            dcc.Input(id='input-humidity', type='number', placeholder='Enter Humidity', className="mb-2 mx-2"),
            dcc.Input(id='input-ph', type='number', placeholder='Enter pH', className="mb-2"),
            dcc.Input(id='input-rainfall', type='number', placeholder='Enter Rainfall', className="mb-2 mx-2"),
            html.Button('Predict Crop', id='predict-button', n_clicks=0, className="btn btn-primary"),
            html.Div(id='prediction-output', className="mt-4")
        ], width=12),
    ]),

    # Scatter plot with dropdowns
    dbc.Row([
        dbc.Col([
            html.H3("Interactive Scatter Plot", className="text-center mt-4"),
            dcc.Dropdown(
                id='x-axis-dropdown',
                options=[{'label': col, 'value': col} for col in df.columns if col != "label"],
                value='temperature',
                placeholder='Select X-axis',
                className="mb-3"
            ),
            dcc.Dropdown(
                id='y-axis-dropdown',
                options=[{'label': col, 'value': col} for col in df.columns if col != "label"],
                value='rainfall',
                placeholder='Select Y-axis',
                className="mb-3"
            ),
            dcc.Graph(id='scatter-plot')
        ], width=12),
    ])
], fluid=True)

# Callback to update the scatter plot based on dropdown selections
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value')]
)
def update_scatter_plot(x_axis, y_axis):
    if x_axis and y_axis:
        fig = px.scatter(
            df,
            x=x_axis,
            y=y_axis,
            color="label",
            title=f"{x_axis} vs {y_axis}",
            hover_data=['label']
        )
        return fig
    return {}

# Callback to make a POST request to the Flask API for predictions
@app.callback(
    Output('prediction-output', 'children'),
    [Input('predict-button', 'n_clicks')],
    [
        State('input-N', 'value'),
        State('input-P', 'value'),
        State('input-K', 'value'),
        State('input-temperature', 'value'),
        State('input-humidity', 'value'),
        State('input-ph', 'value'),
        State('input-rainfall', 'value')
    ]
)
def predict_crop(n_clicks, N, P, K, temperature, humidity, ph, rainfall):
    # Clear the output if no button click
    if n_clicks is None or n_clicks == 0:
        return ""

    # Check for missing inputs
    if None in [N, P, K, temperature, humidity, ph, rainfall]:
        return "⚠️ Please enter all values before predicting."

    # Prepare the data to send in the POST request
    data = {
        'N': N,
        'P': P,
        'K': K,
        'temperature': temperature,
        'humidity': humidity,
        'ph': ph,
        'rainfall': rainfall
    }

    try:
        # Send POST request to the Flask API
        response = requests.post('http://127.0.0.1:5000/predict', json=data)
        prediction = response.json()

        # Get the crop name from the crop mapping
        crop_name = crop_mapping[prediction["prediction"]]

        # Return the crop name as output
        return f'✅ Recommended Crop: {crop_name}'

    except Exception as e:
        return f"❌ Error: {str(e)}"


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
