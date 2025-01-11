# Hiring Assistant Chatbot

## Project Overview
The Hiring Assistant Chatbot is designed to streamline the interview process by gathering candidate details, generating technical questions, and engaging in conversations to assess suitability for roles. It utilizes advanced AI models to provide a seamless and interactive experience for candidates.

## Installation Instructions
Follow these steps to set up and run the application locally:

1. Clone the repository:
    ```sh
    git clone https://github.com/YashPanchal1901/hiring-assistant-chatbot.git
    cd hiring-assistant-chatbot
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set the environment variables for the API keys:
    ```sh
    export GROQ_API_KEY='your_groq_api_key'
    export TAVILY_API_KEY='your_tavily_api_key'
    export GOOGLE_API_KEY='your_google_api_key'
    ```

4. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

## Usage Guide
1. Open your web browser and navigate to the provided local URL (typically `http://localhost:8501`).
2. The chatbot will greet you and provide an overview of its purpose.
3. Fill out the candidate details form and submit it.
4. The chatbot will generate technical questions based on your provided tech stack.
5. Answer the questions and engage in further conversation with the chatbot.
6. At the end of the conversation, the chatbot will provide an emotion analysis of your responses.

## Technical Details
- **Libraries Used**:
  - Streamlit: For building the interactive web interface.
  - LangChain: For managing the conversational flow and memory.
  - TextBlob: For sentiment analysis to determine the emotion of responses.
  - Tavily Search: For advanced search capabilities.
  - OpenAI: For fallback AI model integration.

- **Model Details**:
  - `ChatGroq`: Primary AI model (llama-3.3-70b-versatile).
  - `ChatGoogleGenerativeAI`: Fallback AI model (gemini-1.5-flash).

- **Architectural Decisions**:
  - The application uses a multi-model approach to ensure robust and reliable responses.
  - Conversation memory is maintained using `ConversationBufferMemory` to provide context-aware interactions.
  - Environment variables are used for API keys to enhance security and flexibility.

## Prompt Design
Prompts were carefully crafted to handle information gathering and technical question generation. The prompts ensure that the chatbot can:
- Collect candidate details efficiently.
- Generate relevant technical questions based on the provided tech stack.
- Maintain a context-aware conversation by saving and retrieving previous interactions from memory.

## Challenges & Solutions
### Challenges:
1. **Integrating Multiple AI Models**:
   - Ensuring seamless fallback between primary and secondary models was complex.

2. **Emotion Analysis**:
   - Accurately determining the sentiment of candidate responses required fine-tuning the sentiment analysis model.

3. **Maintaining Context**:
   - Keeping track of conversation history to provide context-aware responses was challenging.

### Solutions:
1. **Model Integration**:
   - Used LangChain's fallback mechanism to switch between models seamlessly.

2. **Improving Sentiment Analysis**:
   - Incorporated TextBlob for sentiment analysis and validated its performance with various test cases.

3. **Effective Memory Management**:
   - Utilized `ConversationBufferMemory` to store and retrieve conversation history, ensuring context-aware interactions.
