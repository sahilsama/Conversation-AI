import os  # For checking file size and existence
import json
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")

Username = env_vars.get("JARVIS")
Assistantname = env_vars.get("Sahil")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key="")

System = f"""Hello, I am Sahil, You are a very accurate and an advanced AI named JARVIS which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, always talk to the point, just answer the question.***
*** Reply in only English, even if the question is in any other languages, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {"role": "system", "content": System}
]

def RealTimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"Please use this real time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours:{minute} minutes:{second} seconds\n"
    return data

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def ChatBot(Query):
    try:
        chat_log_path = r"Data\ChatLog.json"
        messages = []  # Default to an empty list

        # Check if file exists and is not empty
        if os.path.exists(chat_log_path) and os.path.getsize(chat_log_path) > 0:
            with open(chat_log_path, "r") as f:
                try:
                    messages = load(f)  # Attempt to load existing JSON
                except json.JSONDecodeError:
                    # Handle corrupted JSON by resetting the file
                    messages = []
                    with open(chat_log_path, "w") as wf:
                        dump(messages, wf)

        # Process user query
        messages.append({"role": "user", "content": f"{Query}"})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealTimeInformation()}] + messages,
            max_tokens=1204,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")

        messages.append({"role": "assistant", "content": f"{Answer}"})

        # Write updated messages back to file
        with open(chat_log_path, "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer=Answer)

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing your request. Please try again later."

if __name__ == "__main__":
    while True:
        user = input(">>> ")
        print(ChatBot(user))


