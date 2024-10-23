import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import nltk
from flask import Flask, render_template, request

nltk.download('punkt_tab')

app = Flask(__name__)

def create_chatbot():
    bot = ChatBot("Rudra", read_only=False, logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "Sorry, I don't have an answer for this. Please use the FIX-DEVICE option to contact Machinevice.",
            "maximum_similarity_threshold": 0.9
        },
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "Sorry, I couldn't understand that.",
            "maximum_similarity_threshold": 0.8,
            "weight": 1
        },
    ])
    return bot

def train_chatbot(bot):
    with open('training_data.json', 'r') as file:
        data = json.load(file)
        conversations = data['conversations']
    
    with open('training_data_conversation2.json', 'r') as file:
        additional_data = json.load(file)
        additional_conversations = additional_data['conversations']
    
    corpus_trainer = ChatterBotCorpusTrainer(bot)
    list_trainer = ListTrainer(bot)

    corpus_trainer.train("chatterbot.corpus.english")

    for conversation in conversations + additional_conversations:
        list_trainer.train(conversation)

# Create and train the chatbot before starting the app
bot = create_chatbot()
train_chatbot(bot)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/get")
def get_chatbot_response():
    userText = request.args.get('userMessage')
    response = str(bot.get_response(userText))

    # Check for actions based on user input
    actions = []
    if "change wallpaper" in userText.lower():
        actions = [
            {"label": "Open Wallpaper Settings (Windows)", "action": "open_wallpaper_settings_windows"},
            {"label": "Open Wallpaper Settings (Linux)", "action": "open_wallpaper_settings_linux"},
            {"label": "Open Wallpaper Settings (Mac)", "action": "open_wallpaper_settings_mac"}
        ]
    # Add more conditions for other actions as needed

    return json.dumps({"response": response, "actions": actions})

@app.route("/action")
def perform_action():
    action = request.args.get('action')
    
    if action == "open_wallpaper_settings_windows":
        return "Opening wallpaper settings on Windows..."
    elif action == "open_wallpaper_settings_linux":
        return "Opening wallpaper settings on Linux..."
    elif action == "open_wallpaper_settings_mac":
        return "Opening wallpaper settings on macOS..."
    # Add more actions as needed

    return "Action not recognized."

# Main flow
if __name__ == "__main__":
    app.run(debug=True)
