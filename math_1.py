from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Initialize the ChatBot with a mathematical logic adapter
bot = ChatBot(
    "Math",
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation"
    ],
    storage_adapter="chatterbot.storage.SQLStorageAdapter"
)

# Optional: Train the bot (if needed)
# trainer = ChatterBotCorpusTrainer(bot)
# trainer.train("chatterbot.corpus.english")

print("-----Mathematician Rudra-------------")

# Run an infinite loop to get user input and provide responses
while True:
    user_text = input("Type the math equation that you want to solve: ")
    if user_text.lower() == "exit":
        break
    try:
        response = bot.get_response(user_text)
        if response.confidence > 0:  # Check confidence score to ensure valid response
            print("Rudra: " + str(response))
        else:
            print("Rudra: Sorry, I didn't understand the equation. Please try again.")
    except Exception as e:
        print("An error occurred:", e)
