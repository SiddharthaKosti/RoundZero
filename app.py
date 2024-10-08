import streamlit as st
import pyttsx3
import os
import dotenv
import speech_recognition as sr

from src.capture_speech import capture_speech
from src.generate_questions import generate_questions
from src.score_answer import score_answer_opnai, score_answer_litellm

# Initialize pyttsx3 with a more human-like voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Assuming the second voice is more human-like
engine.setProperty('rate', 125)  # Adjust the rate to a more natural speed

# Initialize session state for questions, index, and generation flag
if 'questions' not in st.session_state:
    st.session_state.questions = [
        "What is the full form of AI?",
        "How do you handle exceptions in Python, and what is the purpose of the 'try' and 'except' blocks?",
    ]
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0  # Initialize the index in session state
if 'user_response' not in st.session_state:
    st.session_state.user_response = None  # Store user responses across reruns
if 'questions_generated' not in st.session_state:
    st.session_state.questions_generated = False  # Track if questions have been generated

# Sidebar for topic selection
st.sidebar.title("Select a Topic")
topic = st.sidebar.selectbox("Choose a topic:", ["python", "computer vision", "genai"])

# When the user clicks "Generate Questions"
if st.sidebar.button("Generate Questions"):
    st.session_state.questions_generated = True  # Mark that questions have been generated
    st.write("### Generated Questions:")
    st.write(st.session_state.questions)
    
    # Reset the current question index to 0 when generating questions
    st.session_state.current_question_index = 0
    
    # Display the first question
    if st.session_state.questions:
        st.write("### Current Question:")
        st.write(st.session_state.questions[st.session_state.current_question_index])
        
        # After displaying the question, speak the first question
        engine.say(st.session_state.questions[st.session_state.current_question_index])
        engine.runAndWait()
    
    # Capture user's response
    st.session_state.user_response = capture_speech()

    # Evaluate the user's response
    if st.session_state.user_response is not None:
        get_score_ans = score_answer_litellm(
            st.session_state.questions[st.session_state.current_question_index],
            st.session_state.user_response
        )
        st.divider()
        st.write("SCORE: ", get_score_ans["accuracy_score"])
        st.write("EXPLAINATION: ", get_score_ans["reason"])



# Only show the "Next Question" button if questions have been generated
if st.session_state.questions_generated:
    # Button to proceed to the next question
    if st.button("Next Question"):
        if st.session_state.current_question_index < len(st.session_state.questions) - 1:
            st.session_state.current_question_index += 1  # Update the index in session state
            
            # Display the next question
            st.write("### Current Question:")
            st.write(st.session_state.questions[st.session_state.current_question_index])
            
            # Speak the next question
            engine.say(st.session_state.questions[st.session_state.current_question_index])
            engine.runAndWait()
            
            # Capture user's response for the next question
            st.session_state.user_response = capture_speech()

            # Evaluate the user's response
            if st.session_state.user_response is not None:
                get_score_ans = score_answer_litellm(
                    st.session_state.questions[st.session_state.current_question_index],
                    st.session_state.user_response
                )
                st.divider()
                st.write("SCORE: ", get_score_ans["accuracy_score"])
                st.write("EXPLAINATION: ", get_score_ans["reason"])
        else:
            st.write("No more questions.")
