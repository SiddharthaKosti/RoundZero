import openai
import os
import dotenv
dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_questions(topic):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Generate 2 questions about {topic}. Return the questions in a list. Do not include any other text. Separate each question with a new line."}
        ]
    )
    questions = response.choices[0].message.content.strip().split('\n')
    questions = [question for question in questions if question!=""]
    return questions