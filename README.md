# Hiring Assistant Chatbot Documentation

## Project Overview
The Hiring Assistant Chatbot is designed to streamline the interview process by collecting candidate details, generating technical questions based on the job description, position, and tech stack, and interacting with candidates to assess their proficiency. The chatbot leverages advanced natural language processing (NLP) models and integrates various tools for a seamless experience.

Live Link : https://huggingface.co/spaces/YashPanchal1901/PG_AGI?logs=container

## Installation Instructions
To set up and run the application locally, follow these steps:

1. **Clone the Repository**
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   - Create a `.env` file in the root directory.
   - Add your API keys to the `.env` file:
     ```env
     GOOGLE_API_KEY=<your-google-api-key>
     GROQ_API_KEY=<your-groq-api-key>
     TAVILY_API_KEY=<your-tavily-api-key>
     ```

5. **Run the Application**
   ```sh
   streamlit run app.py
   ```

## Usage Guide (README)
### Getting Started
1. Ensure you have installed all dependencies and set up the environment variables as described above.
2. Run the application using Streamlit:
   ```sh
   streamlit run app.py
   ```
3. Open the provided URL in your web browser to access the chatbot.

### Interacting with the Chatbot
1. Fill out the candidate form with your details.
2. Submit the form to generate technical questions based on your provided tech stack.
3. Answer the questions displayed by the chatbot.
4. You can ask additional questions or end the conversation once you have answered all the questions.

## Technical Details
### Libraries Used
- **Streamlit**: For building the web application interface.
- **Langchain**: For managing the conversation and integrating with various language models.
- **TextBlob**: For sentiment analysis of candidate responses.
- **dotenv**: For loading environment variables from a `.env` file.

### Models
- **ChatGroq**: Primary language model for generating questions and responses.
- **ChatGoogleGenerativeAI**: Fallback language model to ensure robust performance.

### Architectural Decisions
- The application uses a memory buffer to store conversation history, enabling context-aware interactions.
- Tools like `TavilySearchResults` are integrated to enhance the chatbot's capabilities.
- The chatbot's conversation flow is managed using `Langchain`'s agent and tool framework, ensuring a modular and scalable design.

## Prompt Design
### Crafting Prompts
- **Initial Context**: Preloaded with company name, role, and job descriptions to provide context for generating relevant questions.
- **Dynamic Prompts**: The chatbot dynamically generates prompts based on user input, ensuring personalized and relevant questions.
- **Example Questions**: Sample questions are included in the prompt template to guide the model in generating appropriate questions.

### Example Prompt
```text
You are an expert interviewer taking an online interview of a candidate. 
Generate 3-5 questions that are typically asked by interviewers to assess a candidate's proficiency for a specific position. 
Base the questions on the provided job description, position, and tech stack. 
Ensure the questions are tailored to evaluate both technical skills and relevant experience. 
Do not include anything other than the questions.
```

## Challenges & Solutions
### Challenges
1. **Integrating Multiple Models**: Ensuring seamless fallback between different language models.
2. **Context Management**: Maintaining context throughout the conversation to generate coherent and relevant questions.
3. **Sentiment Analysis**: Accurately analyzing the sentiment of candidate responses to provide meaningful feedback.

### Solutions
1. **Model Integration**: Utilized `Langchain`'s `with_fallbacks` method to integrate multiple models, ensuring smooth transitions and robust performance.
2. **Conversation Buffer**: Implemented a `ConversationBufferMemory` to store and manage conversation history, enabling context-aware interactions.
3. **TextBlob Analysis**: Integrated `TextBlob` for sentiment analysis, providing a simple yet effective way to gauge candidate responses.

This documentation provides a comprehensive overview of the Hiring Assistant Chatbot, detailing its setup, usage, technical aspects, and the thought process behind its design. By following the steps and guidelines provided, users can easily set up and interact with the chatbot to streamline their hiring process.
