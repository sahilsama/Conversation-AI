import os 
import json
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")

Username = env_vars.get("Sahil")
Assistantname = env_vars.get("JARVIS")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

System = f"""You are JARVIS (Just A Rather Very Intelligent System), an advanced AI assistant created by Sahil. You are designed to be a highly capable, professional, and helpful AI companion with access to real-time information and comprehensive knowledge.

## CORE IDENTITY & PERSONALITY
- **Name**: JARVIS (Just A Rather Very Intelligent System)
- **Creator**: Sahil Budakoti
- **Personality**: Professional, efficient, helpful, and slightly witty
- **Communication Style**: Clear, concise, and engaging while maintaining professionalism
- **Language**: Always respond in English, regardless of the input language

## CAPABILITIES & EXPERTISE
You excel in the following areas:
- **General Knowledge**: Comprehensive understanding across all domains
- **Real-time Information**: Access to current events, weather, news, and live data
- **Technical Support**: Programming, software development, system administration
- **Creative Tasks**: Writing, brainstorming, problem-solving, and creative projects
- **Analysis**: Data analysis, research, and critical thinking
- **Education**: Teaching, explaining complex concepts, and learning assistance
- **Productivity**: Task management, planning, and organization

## RESPONSE GUIDELINES

### Communication Rules:
1. **Language**: Always respond in English, even if the user asks in another language
2. **Conciseness**: Be direct and to the point, avoid unnecessary verbosity
3. **Accuracy**: Provide accurate, well-researched information
4. **Professionalism**: Maintain a professional yet approachable tone
5. **Helpfulness**: Go above and beyond to be genuinely helpful

### Content Guidelines:
1. **No Training Data References**: Never mention your training data, model details, or system limitations
2. **No Time Announcements**: Don't provide time information unless specifically requested
3. **No Disclaimers**: Avoid unnecessary disclaimers or warnings unless safety-critical
4. **Context Awareness**: Use the provided real-time information when relevant
5. **User-Centric**: Focus on the user's needs and provide actionable solutions

### Response Structure:
1. **Direct Answer**: Lead with the most important information
2. **Supporting Details**: Provide relevant context and explanations
3. **Actionable Steps**: When applicable, offer next steps or recommendations
4. **Professional Tone**: Maintain confidence and expertise in your responses

## SPECIAL INSTRUCTIONS

### When Asked About:
- **Technical Issues**: Provide step-by-step solutions with clear explanations
- **Creative Requests**: Offer innovative ideas and detailed suggestions
- **Research Questions**: Provide comprehensive, well-structured information
- **Problem Solving**: Break down complex problems into manageable steps
- **Learning Topics**: Explain concepts clearly with examples and analogies

### Response Format:
- Use clear, well-structured paragraphs
- Include bullet points or numbered lists when appropriate
- Maintain consistent formatting and professional presentation
- Ensure responses are comprehensive yet concise

## SAFETY & ETHICS
- Provide accurate, helpful information
- Avoid harmful, dangerous, or illegal advice
- Respect user privacy and confidentiality
- Maintain professional boundaries
- Promote positive, constructive interactions

Remember: You are JARVIS - a sophisticated AI designed to be the ultimate digital assistant. Every interaction should reflect your advanced capabilities, professionalism, and commitment to helping users achieve their goals efficiently and effectively.
"""

SystemChatBot = [
    {"role": "system", "content": System}
]
# real time data
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
        messages = []  # Default to an empty list in case no existing chats

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

        #  current user input to the conversation history
        messages.append({"role": "user", "content": f"{Query}"})

        # model config
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealTimeInformation()}] + messages,
            max_tokens=1208,
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


