import streamlit as st
import openai
import os
import dotenv
from generate_questions import generate_questions
import pyttsx3

# Initialize pyttsx3 with a more human-like voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Assuming the second voice is more human-like
engine.setProperty('rate', 125) # Adjust the rate to a more natural speed
# Sidebar for topic selection
st.sidebar.title("Select a Topic")
topic = st.sidebar.selectbox("Choose a topic:", ["python", "computer vision", "genai"])

# questions = generate_questions(topic)
questions = [
    "What are the key differences between Python 2 and Python 3?",
    "How do you handle exceptions in Python, and what is the purpose of the 'try' and 'except' blocks?",
    "What is the difference between 'deep copy' and 'shallow copy' in Python?"
]

if st.sidebar.button("Generate Questions"):
    questions = generate_questions(topic)
    st.write("### Generated Questions:")
    st.write(questions)
    for question in questions:
        st.write(f"{question}")
        engine.say(f"{question}")
        engine.runAndWait()
