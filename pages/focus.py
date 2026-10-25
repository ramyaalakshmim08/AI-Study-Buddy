import streamlit as st
import time
from datetime import date
from database import get_connection


def save_study_session(duration):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO study_sessions
        (subject, duration, session_date)
        VALUES (?, ?, ?)
        """,
        ("Focus Session", duration, str(date.today()))
    )

    connection.commit()
    connection.close()


def render_focus():

    st.title("Focus")
    st.write("Stay focused with a simple study timer.")

    st.divider()

    if "focus_running" not in st.session_state:
        st.session_state.focus_running = False

    if "focus_seconds" not in st.session_state:
        st.session_state.focus_seconds = 25 * 60

    if "focus_duration" not in st.session_state:
        st.session_state.focus_duration = 25

    # Custom duration
    duration = st.number_input(
        "Focus duration (minutes)",
        min_value=1,
        max_value=180,
        value=25,
        step=1,
        disabled=st.session_state.focus_running
    )

    # Update timer duration before starting
    if not st.session_state.focus_running:

        if duration != st.session_state.focus_duration:

            st.session_state.focus_duration = int(duration)

            st.session_state.focus_seconds = int(
                duration * 60
            )

    minutes = st.session_state.focus_seconds // 60
    seconds = st.session_state.focus_seconds % 60

    st.markdown(
        f"# {minutes:02d}:{seconds:02d}"
    )

    col1, col2 = st.columns(2)

    with col1:

        if not st.session_state.focus_running:

            if st.button(
                "Start",
                use_container_width=True
            ):

                st.session_state.focus_running = True
                st.rerun()

        else:

            if st.button(
                "Pause",
                use_container_width=True
            ):

                st.session_state.focus_running = False
                st.rerun()

    with col2:

        if st.button(
            "Reset",
            use_container_width=True
        ):

            st.session_state.focus_running = False

            st.session_state.focus_seconds = int(
                st.session_state.focus_duration * 60
            )

            st.rerun()

    # Countdown
    if st.session_state.focus_running:

        time.sleep(1)

        st.session_state.focus_seconds -= 1

        if st.session_state.focus_seconds <= 0:

            st.session_state.focus_seconds = 0
            st.session_state.focus_running = False

            save_study_session(
                st.session_state.focus_duration
            )

            st.success(
                "Focus session completed."
            )

        st.rerun()