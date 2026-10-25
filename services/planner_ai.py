from google import genai
import streamlit as st


client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


def generate_study_plan(
    subject,
    topic,
    days_remaining,
    daily_minutes,
    priority
):

    prompt = f"""
You are an AI Study Planner for a college student.

Create a practical and personalized study plan.

Subject: {subject}
Topic: {topic}
Days available: {days_remaining}
Study time per day: {daily_minutes} minutes
Priority: {priority}

Requirements:
- Create a day-by-day study plan.
- Divide the topic into logical learning sections.
- Include learning, practice, and revision where appropriate.
- Respect the available study time each day.
- Keep the plan realistic for a college student.
- Use clear headings and bullet points.
- Do not invent specific syllabus topics if the provided topic is broad.
- End with a short final revision strategy.
"""

    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt
    )

    return interaction.output_text