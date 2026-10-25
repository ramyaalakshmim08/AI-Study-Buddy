from google import genai
import streamlit as st


client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


def generate_answer(question, context, study_mode):

    mode_instructions = {
        "Ask a Question":
            "Answer the student's question clearly and directly.",

        "Explain a Concept":
            "Teach the concept step by step using simple language and a small example.",

        "Summarize":
            "Summarize the important points concisely using bullet points.",

        "Exam Answer":
            "Write a well-structured exam-ready answer with definition, key points, and example where appropriate.",

        "Generate Quiz":
            "Create 5 questions based only on the provided study material. Include the answers after the questions."
    }

    instruction = mode_instructions.get(
        study_mode,
        "Answer the student's question clearly."
    )

    prompt = f"""
You are an AI Study Buddy helping a college student learn.

Study Material:
{context}

Student Question or Topic:
{question}

Study Mode:
{study_mode}

Instructions:
{instruction}

Additional rules:
- Use the provided study material as the main source.
- Do not invent information that is not supported by the material.
- If the material does not contain enough information, clearly say so.
- Keep the response educational and easy to understand.
"""

    interaction = client.interactions.create(
       model="gemini-3.5-flash-lite",
        input=prompt
    )

    return interaction.output_text