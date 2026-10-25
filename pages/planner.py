import streamlit as st
from datetime import date

from services.planner_ai import generate_study_plan


def render_planner():

    st.title("Study Planner")

    st.write(
        "Create a focused study plan based on your upcoming academic priorities."
    )

    st.divider()

    st.subheader("Plan Your Study")

    subject = st.text_input(
        "Subject",
        placeholder="Example: Java Programming"
    )

    topic = st.text_input(
        "Topic",
        placeholder="Example: Object-Oriented Programming"
    )

    exam_date = st.date_input(
        "Exam / Target Date",
        min_value=date.today()
    )

    daily_minutes = st.number_input(
        "Available study time per day (minutes)",
        min_value=15,
        max_value=480,
        value=60,
        step=15
    )

    priority = st.selectbox(
        "Priority",
        ["High", "Medium", "Low"]
    )

    if st.button(
        "Create Study Plan",
        use_container_width=True
    ):

        if not subject.strip() or not topic.strip():

            st.warning(
                "Please enter both the subject and topic."
            )

        else:

            today = date.today()

            days_remaining = (
                exam_date - today
            ).days

            if days_remaining == 0:
                days_remaining = 1

            st.success(
                "Study plan created."
            )

            st.divider()

            st.subheader(
                "Your Study Plan"
            )

            st.write(
                f"**Subject:** {subject}"
            )

            st.write(
                f"**Topic:** {topic}"
            )

            st.write(
                f"**Priority:** {priority}"
            )

            st.write(
                f"**Days available:** {days_remaining}"
            )

            st.write(
                f"**Daily study time:** {daily_minutes} minutes"
            )

            total_minutes = (
                days_remaining * daily_minutes
            )

            st.metric(
                "Planned Study Time",
                f"{total_minutes} min"
            )

            st.divider()

            st.subheader(
                "AI-Generated Study Plan"
            )

            with st.spinner(
                "Creating your personalized study plan..."
            ):

                try:

                    ai_plan = generate_study_plan(
                        subject,
                        topic,
                        days_remaining,
                        daily_minutes,
                        priority
                    )

                    st.write(ai_plan)

                except Exception as error:

                    st.error(
                        f"Unable to generate the study plan: {error}"
                    )