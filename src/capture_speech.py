import speech_recognition as sr
import streamlit as st
    
def capture_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please speak your answer...")
        audio = recognizer.listen(source)
        try:
            response = recognizer.recognize_google(audio)
            st.write(f"You said: {response}")
            return response
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            st.write("Could not request results from Google Speech Recognition service.")
            return None