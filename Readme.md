

![Screenshot 2025-01-13 211505](https://github.com/user-attachments/assets/5ea57779-1461-4dd8-919a-ae05b702445f)




## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r Requirments.txt
    ```

4. Set up the environment variables in the [.env](http://_vscodecontentref_/23) file:
    ```env
    CohereAPIKey = "your-cohere-api-key"
    GroqAPIKey = "your-groq-api-key"
    HuggingFaceAPIKey = "your-huggingface-api-key"
    Assistantname = "JARVIS"
    Username = "YourName"
    InputLanguage = "en"
    AssistantVoice = "en-GB-RyanNeural"
    ```

## Usage

1. Run the main script to start the AI assistant:
    ```sh
    python Main.py
    ```

2. Interact with JARVIS through the graphical user interface or via voice commands.

## Features

- **Automation**: Open and close applications, play YouTube videos, and more.
- **Chatbot**: Engage in conversations and get answers to general queries.
- **Real-time Search**: Retrieve up-to-date information from the internet.
- **Content Generation**: Generate content like letters, essays, and more.
- **Speech Recognition**: Convert speech to text using the microphone.
- **Text-to-Speech**: Convert text responses to speech.
- **WhatsApp Automation**: Send messages via WhatsApp.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
