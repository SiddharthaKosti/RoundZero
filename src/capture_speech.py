import speech_recognition as sr
import streamlit as st

def capture_speech():
    recognizer = sr.Recognizer()

    # Adjust thresholds for longer listening and detection time
    recognizer.pause_threshold = 1.0  # Time to pause between words
    recognizer.energy_threshold = 300  # Energy level for ambient noise
    
    attempts = 3  # Number of attempts to capture speech
    for attempt in range(attempts):
        with sr.Microphone() as source:
            st.write("Please speak your answer...")
            audio = recognizer.listen(source, timeout=20)

            try:
                response = recognizer.recognize_google(audio)
                st.write(f"You said: {response}")
                return response
            except sr.UnknownValueError:
                st.write("Sorry, I could not understand the audio.")
                if attempt < attempts - 1:  # If not the last attempt
                    st.write("Please try again.")
            except sr.RequestError:
                st.write("Could not request results from Google Speech Recognition service.")
                return None
    st.write("Failed to capture the answer after multiple attempts.")
    return None