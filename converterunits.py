from chatterbot import ChatBot

# Initialize the ChatBot with a unit conversion logic adapter
bot = ChatBot(
    "units",
    logic_adapters=[
        'chatterbot.logic.UnitConversion'
    ],
    storage_adapter="chatterbot.storage.SQLStorageAdapter"
)

print("----- Unit Conversion Assistant -----")
print("Type 'exit' to quit the program.")

# Run an infinite loop to get user input and provide responses
while True:
    user_text = input("Ask a unit conversion (e.g., 'convert 5 miles to kilometers'): ")
    if user_text.lower() == "exit":
        print("Thank you for using the Unit Conversion Assistant. Goodbye!")
        break
    try:
        # Get the chatbot's response
        chatbot_response = bot.get_response(user_text)
        if chatbot_response:  # Check if the response is not None
            print("Result:", str(chatbot_response))
        else:
            print("Sorry, I couldn't process that conversion. Please try again.")
    except Exception as e:
        print("An error occurred:", e)
