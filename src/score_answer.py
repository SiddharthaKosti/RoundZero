import streamlit as st
import openai
import os
import re
import json
import litellm
import dotenv
dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def create_evaluator_prompt(question, answer):
    return [
            {
                "role": "system",
                "content": "You are a Question Answer evaluator. Given a set of Question/Answer pair, "
                        "you identify the correctness of the answer for that question."
            },
            {
                "role": "user",
                "content": f"""This is the question: {question}

            This is the Answer: {answer}

            Return the answer in JSON format without any extra text:
            {{
                "accuracy_score": "float between 0.0 and 1.0",
                "reason": "explanation for the score"
            }}"""
            }
        ]

def get_cleaned_response(response):
    cleaned_response = re.sub(r'^```json\n|\n```$', '', response.strip())
    cleaned_answer = json.loads(cleaned_response)
    return cleaned_answer

def score_answer_litellm(question, answer):
    evaluator_prompt = create_evaluator_prompt(question, answer)
    response = litellm.completion(
        model="gpt-4o-mini",
        messages=evaluator_prompt
    )
    try:
        response = response.choices[0].message.content        
        return get_cleaned_response(response)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON response"}


def score_answer_openai(question, answer):
    evaluator_prompt = create_evaluator_prompt(question, answer)
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=evaluator_prompt
    )
    try:
        response = response.choices[0].message.content
        return get_cleaned_response(response)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON response"}
