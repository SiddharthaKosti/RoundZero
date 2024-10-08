import streamlit as st
import openai
import os
import dotenv
import pyttsx3
import speech_recognition as sr

from src.capture_speech import capture_speech
from src.generate_questions import generate_questions


# Initialize pyttsx3 with a more human-like voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Assuming the second voice is more human-like
engine.setProperty('rate', 125) # Adjust the rate to a more natural speed

# Initialize session state for questions and index
if 'questions' not in st.session_state:
    st.session_state.questions = [
        "What is the full form of AI?",
        "How do you handle exceptions in Python, and what is the purpose of the 'try' and 'except' blocks?",
        # "What is the difference between 'deep copy' and 'shallow copy' in Python?"
    ]
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0  # Initialize the index in session state

# Sidebar for topic selection
st.sidebar.title("Select a Topic")
topic = st.sidebar.selectbox("Choose a topic:", ["python", "computer vision", "genai"])

if st.sidebar.button("Generate Questions"):
    st.write("### Generated Questions:")
    st.write(st.session_state.questions)
    
    # Reset the current question index to 0 when generating questions
    st.session_state.current_question_index = 0
    # Display the current question if questions are available
    if st.session_state.questions:
        st.write("### Current Question:")
        st.write(st.session_state.questions[st.session_state.current_question_index])
    
    # Speak the first question
    engine.say(st.session_state.questions[st.session_state.current_question_index])
    engine.runAndWait()
    
    # Capture user's response
    user_response = capture_speech()


    # Button to proceed to the next question
    if st.button("Next Question"):
        if st.session_state.current_question_index < len(st.session_state.questions) - 1:
            st.session_state.current_question_index += 1  # Update the index in session state
            engine.say(st.session_state.questions[st.session_state.current_question_index])
            engine.runAndWait()
            user_response = None  # Reset the response for the next question
        else:
            st.write("No more questions.")
