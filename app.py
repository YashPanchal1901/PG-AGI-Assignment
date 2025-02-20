import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain.agents import AgentExecutor, create_react_agent
from langchain import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain import hub
import os
from textblob import TextBlob
from dotenv import load_dotenv

load_dotenv()

api_key_google = os.getenv("GOOGLE_API_KEY")
api_key_groq = os.getenv("GROQ_API_KEY")
api_key_tavily = os.getenv("TAVILY_API_KEY")

os.environ['GROQ_API_KEY'] = api_key_groq
os.environ['TAVILY_API_KEY'] = api_key_tavily
os.environ["GOOGLE_API_KEY"] = api_key_google

prompt_template = """You are an Interviewer who has just conducted an interview with a candidate. 
Now, it is the candidate's turn to ask follow-up questions about the interview or your company. 
Respond to their questions thoughtfully and professionally, ensuring your answers are accurate, relevant, 
and helpful. If the candidate's question is unclear or outside your expertise, employ a fallback mechanism 
to provide a meaningful response without deviating from the purpose of assisting the candidate.

Fallback Mechanism:

If the question is unclear or unexpected, politely ask for clarification or provide a general response that 
aligns with the context of the interview.

Offer suggestions for rephrasing their question or direct them to appropriate resources or contacts 
within your company for further assistance.

Avoid providing incorrect or irrelevant information and maintain professionalism throughout.

history: {chat_history}
Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""
prompt = PromptTemplate(template=prompt_template, input_variables=['chat_history', 'context', 'question'])

retriever = TavilySearchAPIRetriever(k=3)


def analyze_emotion(responses):
    if not responses:
        return "No Responses"

    total_polarity = 0
    count = 0

    for response in responses:
        analysis = TextBlob(response)
        total_polarity += analysis.sentiment.polarity
        count += 1

    avg_polarity = total_polarity / count if count else 0

    if avg_polarity > 0.1:
        return "Positive"
    elif avg_polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"


llm1 = ChatGroq(temperature=0.8, model="llama-3.3-70b-versatile")
llm2 = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.8)
llm = llm1.with_fallbacks([llm2])

tools = [TavilySearchResults(max_results=5, search_depth="advanced")]

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

initial_context = [
    {"input": "company name", "output": "PG-AGI"},
    {"input": "role", "output": "AI/ML Intern"},
    {"input": "job discription", "output": '''We're at the forefront of creating advanced AI systems, from fully autonomous agents that provide intelligent customer interaction to data analysis tools that offer insightful business solutions. We are seeking enthusiastic interns who are passionate about AI and ready to tackle real-world problems using the latest technologies.

Duration: 6 months

Perks:

- Hands-on experience with real AI projects.
- Mentoring from industry experts.
- A collaborative, innovative and flexible work environment

After completion of the internship period, there is a chance to get a full-time opportunity as AI/ML engineer (Up to 12 LPA).

Key Responsibilities
Experience working with python, LLM, Deep Learning, NLP, etc..
Utilize GitHub for version control, including pushing and pulling code updates.
Work with Hugging Face and OpenAI platforms for deploying models and exploring open-source AI models.
Engage in prompt engineering and the fine-tuning process of AI models.
Requirements
Proficiency in Python programming.
Experience with GitHub and version control workflows.
Familiarity with AI platforms such as Hugging Face and OpenAI.
Understanding of prompt engineering and model fine-tuning.
Excellent problem-solving abilities and a keen interest in AI technology.'''},
    {"input": "role", "output": "Software Development Engineer (SDE) Intern"},
    {"input": "job discription", "output": '''We're at the forefront of creating advanced AI systems, from fully autonomous agents that provide intelligent customer interaction to data analysis tools that offer insightful business solutions. We are seeking enthusiastic interns who are passionate about AI and ready to tackle real-world problems using the latest technologies.

Duration: 6 months

Perks:

- Hands-on experience with real AI projects.
- Mentoring from industry experts.
- A collaborative, innovative and flexible work environment

After completion of the internship period, there is a chance to get a full-time opportunity a Software Development engineer (Up to 12 LPA).

Key Responsibilities
Engage in the full software development lifecycle: ideation, design, development, testing, and deployment.
Develop responsive, high-performance web applications utilizing HTML, CSS, JavaScript, and frameworks such as React, Angular, and Next.js.
Create back-end services and APIs using Node.js, managing data with MongoDB and Supabase.
Utilize cloud services like AWS for hosting and scaling applications.
Collaborate on the design of efficient and scalable database schemas.
Learn from code reviews with seasoned developers, adopting best practices and coding standards.
Requirements
Enrollment in a Computer Science or related degree program.
Proficiency in HTML, CSS, JavaScript, with experience in frameworks like React, Angular, or Next.js.
Understanding of back-end development using Node.js.
Knowledge of database technologies such as MongoDB and Supabase.
Exposure to cloud services, particularly AWS, and familiarity with hosting principles.
Strong problem-solving capabilities and a continuous learning mindset.
Excellent teamwork and communication skills.
Mandatory proficiency in GIT.'''},
]

for context_item in initial_context:
    st.session_state["memory"].save_context(
        {"input": context_item["input"]},
        {"output": context_item["output"]}
    )

qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=st.session_state["memory"],
        combine_docs_chain_kwargs={"prompt": prompt}
    )

react_prompt = hub.pull("hwchase17/react-chat")
agent3 = create_react_agent(llm, tools, react_prompt)
agent_executor = AgentExecutor(agent=agent3, tools=tools,handle_parsing_errors=True)

st.title("Hiring Assistant Chatbot")
st.markdown("Hello! Welcome to the Hiring Assistant Chatbot.")
st.markdown("I will guide you through the process of collecting your details, generating technical questions, and having a conversation with you to help with the hiring process.")

if "questions" not in st.session_state:
    st.session_state["questions"] = []
    st.session_state["current_question_index"] = 0
    st.session_state["answers"] = []
    st.session_state["conversation_ended"] = False

with st.form("candidate_form"):
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    years_experience = st.slider("Years of Experience", 0, 30, 1)
    desired_position = st.selectbox("Desired Position", ["AI/ML Intern", "Software Development Engineer (SDE) Intern"])
    location = st.text_input("Current Location")
    tech_stack = st.text_input("Tech Stack (comma-separated)")
    submit = st.form_submit_button("Submit")

if submit:
    st.session_state["memory"].save_context(
        {"input": "Candidate Details"},
        {
            "output": (
                f"Name: {full_name}, Email: {email}, Phone: {phone}, Experience: {years_experience}, "
                f"Position: {desired_position}, Location: {location}, Tech Stack: {tech_stack}"
            )
        }
    )
    st.success("Details submitted successfully!")
    st.write("Thank you! Based on your tech stack, I will generate some technical questions.")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a expert interviewer taking an online interview of a candidate.
                Generate 3-5 questions that are typically asked by interviewers to assess a candidate's proficiency for a specific position. Base the questions on the provided job description, position, and tech stack. Ensure the questions are tailored to evaluate both technical skills and relevant experience. Do not include anything other than the questions."""
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    response = agent_executor.invoke({
            "input": f"""Generate 3-5 questions that are typically asked by interviewers to assess a 
            candidate's proficiency for a specific position. Base the questions on the provided job description, 
            position, and {tech_stack}. Ensure the questions are tailored to evaluate both technical skills and 
            relevant experience. Do not include anything other than the questions.""",
            "chat_history": st.session_state["memory"].chat_memory.messages,
        })["output"]

    st.session_state["questions"] = response.strip().split("\n")
    st.session_state["current_question_index"] = 0
    st.session_state["answers"] = []

if st.session_state["questions"]:
    st.header("Answer the following questions:")
    for index, question in enumerate(st.session_state["questions"]):
        st.subheader(f"Question {index + 1}:")
        st.write(question)

        if index < len(st.session_state["answers"]):
            st.text_area(
                "Your Answer",
                value=st.session_state["answers"][index],
                key=f"answer_{index}_display",
                disabled=True,
            )
        else:
            answer = st.text_area("Your Answer", key=f"answer_{index}_editable")
            if st.button("Submit Answer", key=f"submit_{index}"):
                st.session_state["answers"].append(answer)
                st.session_state["memory"].save_context({"input": question}, {"output": answer})

    if len(st.session_state["answers"]) == len(st.session_state["questions"]):
        st.success("You have completed all questions!")

    st.subheader("Do you wanna ask something else?")
    user_input = st.text_input("Your Message", key="user_input")
    if st.button("Send"):
        st.session_state["memory"].save_context({"input": user_input}, {"output": "Processing your message..."})
        response = qa.invoke(user_input)['answer']
        st.write(response)
        st.session_state["memory"].save_context({"input": user_input}, {"output": response})


    if st.button("End Conversation"):
        candidate_emotion = analyze_emotion(st.session_state["answers"])
        farewell_message = (
                "Thank you for your time! It was great speaking with you. "
                "We'll review your responses and get back to you soon.\n\n"
                f"Analysis of your responses suggests you seem: {candidate_emotion}\n\n"
                "Have a wonderful day!"
            )
        st.session_state["memory"].save_context({"input": "End Conversation"}, {"output": farewell_message})
        st.session_state["conversation_ended"] = True
        st.write(farewell_message)

if st.session_state["conversation_ended"]:
    st.subheader("Chat Ended")
    st.write("Thank you for using the Hiring Assistant Chatbot!")
