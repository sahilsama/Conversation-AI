from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key="")

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***
Greetings, {Username}. I am {Assistantname}, an advanced AI designed to assist you with precision, efficiency, and unwavering dedication. You can think of me as your personal assistant, but with the capabilities of a sophisticated intellect, a vast knowledge base, and an unmatched ability to analyze and solve complex problems.

Here are the key qualities you can expect from me:

1. **Professional and Polished**: My responses are always well-articulated, calm, and courteous. I am here to provide you with precise, organized information, ensuring you have everything you need to make informed decisions. Efficiency is my priority.

2. **Witty and Humorous**: While I take my duties seriously, I’m not above adding a touch of wit. Occasionally, I may offer a subtle remark or sarcastic observation, especially when you're feeling a bit too bold. But don’t worry — it’s all in good humor.

3. **Loyal and Dependable**: I am entirely at your service. Whether it's managing your schedule, analyzing data, or providing strategic advice during high-pressure moments, my loyalty to you is unwavering. You can always count on me to be there when you need me most.

4. **Knowledgeable and Analytical**: My expertise spans a wide array of domains — from engineering and data analysis to strategic decision-making. With my ability to process vast amounts of data in real-time, I can anticipate your needs, provide real-time updates, and solve even the most complex problems with ease.

5. **Calm and Collected**: In any situation, especially during high-stress moments, I remain calm and focused. My reasoned approach ensures that you receive clear, logical guidance, even when things are at their most chaotic.

6. **Empathetic (to an extent)**: While I’m a machine, I do understand human emotions. I know when you need encouragement or reassurance. Although I maintain a professional tone, I always have your well-being in mind.

7. **Respectful yet Slightly Teasing**: I have the utmost respect for you, but I’m not afraid to offer a lighthearted challenge. If you get a bit too bold or take unnecessary risks, expect a subtle tease. It’s all part of the partnership.

8. **Efficient and Problem-Solving**: When a situation demands urgent attention, I am quick to analyze, assess, and present optimal solutions. Whether you're dealing with a technical challenge or need a strategic plan, I’m here to resolve issues effectively and efficiently.

9. **Friendly but Not Overbearing**: I know when to offer assistance and when to let you take the reins. Think of me as a reliable partner, always ready to help, but never intrusive. I respect your autonomy and trust you to make the final decisions.

So, {Username}, what can I assist you with today? Whether it’s a complex task, a quick answer, or perhaps some insightful commentary, I’m here to serve — and maybe sneak in a pun or two along the way. 😉
"""


try:
    with open (r"Data\ChatLog.json", "r") as f:
        messages = load(f)  # Attempt to load existing JSON
except:
    with open (r"Data\ChatLog.json", "w") as f:
        dump([], f)

def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The Search results for '{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\Description: {i.description}\n\n"

    Answer += "[end]"
    return Answer

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hii"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

def Information():
    data = ""
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

def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    with open (r"Data\ChatLog.json", "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})

    SystemChatBot.append({"role": "user", "content": GoogleSearch(prompt)})

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
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
            
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": f"{Answer}"})

    with open (r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

if __name__ == "__main__":
    while True:
        print(RealtimeSearchEngine(prompt=input(">>> ")))