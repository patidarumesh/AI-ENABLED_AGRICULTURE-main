from flask import Flask, render_template, request, jsonify, g
from fuzzywuzzy import fuzz
import numpy as np
import pandas as pd
from joblib import load
from gemini import OpenRouter

class ContextAwareGeminiChatbot:
    def __init__(self, api_key, model):
        self.gemma_client = OpenRouter(api_key=api_key, model=model)
        self.context = ""

    def interact(self, input_text):
        crop_keywords = ['rice', 'maize', 'chickpea', 'kidneybeans', 'Arhar/Tur',
                         'mothbeans', 'Moong', 'Urad', 'Masoor', 'pomegranate',
                         'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple',
                         'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee', "crop",
                         "farming", "agriculture", "harvest", "planting", "cultivation", "yield",
                         "farmer", "field", "wheat", "weeds", "management", "insect", "water", "irrigation", "crop",
                         "temperature", "humidity", "rainfall", "ph", "nitrogen", "phosphorus", "potassium", "soil",
                         "fertilizer", "pesticide", "disease", "insect", "weed", "harvest", "crop", "storage", "crop",
                         "price", "insurance", "loan", "crop", "subsidy", "crop", "spacing", "export", "crop", "crop",
                         "market", "crop", "weather", "forecast", "farming", "harvest", "agronomy", "agricultural",
                         "cultivation", "irrigation", "soil", "seeds", "pesticides", "fertilizers", "rotation",
                         "machinery", "livestock", "horticulture", "agribusiness", "sustainability", "greenhouse",
                         "organic", "hydroponics", "GMOs", "yield", "planting", "harvesting", "agroecology", "security",
                         "economics", "insurance", "policy", "protection", "forestry", "management", "technology",
                         "commodity", "weather", "forecasting", "development", "biotechnology", "production",
                         "extension", "subsidies", "education", "processing", "mechanization", "finance", "tourism",
                         "waste", "distribution", "systems", "diversity", "genetics", "improvement", "economy",
                         "preservation", "safety", "certification", "ecosystem", "sovereignty", "labor", "land",
                         "industrial", "pathogens", "labeling", "deserts", "terrorism", "biosecurity", "markets",
                         "justice", "statistics", "innovation", "biodynamic", "insecurity", "modeling",
                         "agroecological", "organization", "consumption", "security", "prices", "labeling", "miles"]
        # Filter out responses containing any of the crop-related keywords
        input_with_context = self.context + " " + input_text
        if any(word in input_text.lower() for word in crop_keywords):
            input_with_context = self.context + " " + input_text
            response = self.gemma_client.create_chat_completion(input_with_context)
            return response
        else:
            return "Please ask something related to crops or agriculture."
app = Flask(__name__)

# Load the machine learning model and encoder
Random_model = load('model.pkl')
label_en = load('encode.pkl')

# Load crop details
details_data = pd.read_json('crop_details.json')

# Define columns for input data
columns = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
# Get API from here: https://openrouter.ai/
# @app.before_request
# def before_request():
#     g.chatbot = ContextAwareGeminiChatbot(api_key="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", model="google/gemma-7b-it:free")

@app.route('/', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def crop_data():
    a = None
    spacing = None
    timeofsowing = None
    methodofsowing = None
    timeofwater = None
    nutrientrecommendation = None
    weedmanagement = None
    insectmanagement = None
    diseasemanagement = None
    strawyield = None

    if request.method == "POST":
        N = request.form.get("nitrogen")
        P = request.form.get("phosphorus")
        K = request.form.get("potassium")
        temperature = request.form.get("temperature")
        humidity = request.form.get("humidity")
        ph = request.form.get("ph")
        rainfall = request.form.get("rainfall")

        data = pd.DataFrame(columns=columns)
        data["N"] = [N]
        data["P"] = [P]
        data["K"] = [K]
        data["temperature"] = [temperature]
        data["humidity"] = [humidity]
        data["ph"] = [ph]
        data["rainfall"] = [rainfall]

        pred = Random_model.predict(data)
        a = label_en.inverse_transform(pred)
        a = str(a)[2:-2]

        for crop_name in details_data.name:
            word = crop_name
            if fuzz.ratio(word, a) >= 70:
                spacing = np.array_str(details_data[details_data.name == crop_name].spacing.values)
                timeofsowing = np.array_str(details_data[details_data.name == crop_name].timeOfSowing.values)
                methodofsowing = np.array_str(details_data[details_data.name == crop_name].methodOfSowing.values)
                timeofwater = np.array_str(details_data[details_data.name == crop_name].timeOfWater.values)
                nutrientrecommendation = np.array_str(
                    details_data[details_data.name == crop_name].nutrientRecommendation.values)
                weedmanagement = np.array_str(details_data[details_data.name == crop_name].weedManagement.values)
                insectmanagement = np.array_str(
                    details_data[details_data.name == crop_name].insectManagement.values)
                diseasemanagement = np.array_str(
                    details_data[details_data.name == crop_name].diseaseManagement.values)
                strawyield = np.array_str(details_data[details_data.name == crop_name].strawYield.values)

                spacing = spacing[2:-2]
                timeofsowing = timeofsowing[2:-2]
                methodofsowing = methodofsowing[2:-2]
                timeofwater = timeofwater[2:-2]
                nutrientrecommendation = nutrientrecommendation[2:-2]
                weedmanagement = weedmanagement[2:-2]
                insectmanagement = insectmanagement[2:-2]
                diseasemanagement = diseasemanagement[2:-2]
                strawyield = strawyield[2:-2]
                break

        return render_template("index.html", a=a, spacing=spacing, timeofsowing=timeofsowing,
                               methodofsowing=methodofsowing, timeofwater=timeofwater,
                               nutrientrecommendation=nutrientrecommendation, weedmanagement=weedmanagement,
                               insectmanagement=insectmanagement, diseasemanagement=diseasemanagement,
                               strawyield=strawyield)

    return render_template("index.html")
    return render_template("index.html")
@app.route('/chatBot', methods=['POST', 'GET'])

def indexChat():
    return render_template('chat.html')





import markdown
from bs4 import BeautifulSoup

def markdown_to_plain_text(markdown_text):
    html = markdown.markdown(markdown_text)
    # Convert HTML to plain text
    plain_text = ''.join(BeautifulSoup(html, "html.parser").findAll(text=True))
    return plain_text


@app.before_request
def before_request():
    g.chatbot = ContextAwareGeminiChatbot(api_key="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", model="google/gemma-7b-it:free")

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    user_input = request.json['message']
    if user_input.lower() == 'exit':
        return jsonify({'response': "Goodbye!"})
    response = g.chatbot.interact(user_input)
    plain_text = markdown_to_plain_text(response)
    return jsonify({'response': plain_text})


if __name__ == '__main__':
    app.run(debug=True)
