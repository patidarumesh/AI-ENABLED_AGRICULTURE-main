# AI Enabled Agriculture

This repository contains a Flask web application that integrates a context-aware chatbot powered by Gemini, an AI model developed for natural language processing tasks. The chatbot is tailored for providing information and assistance related to crops and agriculture.

## Features

- **Context Awareness**: The chatbot is capable of understanding the context of the conversation to provide relevant responses, particularly focusing on topics related to crops and agriculture.
- **Crop Information**: Given input parameters related to agricultural conditions (e.g., nitrogen, phosphorus, etc.), the chatbot predicts suitable crops and provides detailed information about them, including recommended spacing, time of sowing, method of sowing, etc.
- **Interactive Chat Interface**: Users can interact with the chatbot through a user-friendly web interface.
- **Chat History**: Users can engage in ongoing conversations with the chatbot and view previous interactions.

## Getting Started

Follow these instructions to set up the project on your local machine:

### Prerequisites

- Python 3.x installed on your system
- Flask and other required Python libraries installed (`flask`, `fuzzywuzzy`, `numpy`, `pandas`, `joblib`, `gemini`)

### Installation

1. Clone this repository to your local machine:

   ```
   git clone <repository_url>
   ```

2. Install the required Python dependencies using pip


### Usage

1. Run the Flask application:

   ```
   python app.py
   ```

2. Access the application through your web browser at `http://localhost:5000`.

## Additional Information

- **Machine Learning Model**: The application incorporates a machine learning model for predicting suitable crops based on input agricultural conditions. Make sure the model files (`model.pkl` and `encode.pkl`) are available in the project directory.
- **Crop Details**: Crop details are loaded from a JSON file (`crop_details.json`). Ensure the file is correctly formatted and contains the necessary information.
- **Web Interface**: The web interface allows users to input agricultural conditions and receive recommendations. Additionally, there's a chat feature where users can engage in conversations with the chatbot.

