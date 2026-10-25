import streamlit as st
from database import get_connection


def get_progress_data():

    connection = get_connection()
    cursor = connection.cursor()

    # Focus time
    cursor.execute("""
        SELECT COALESCE(SUM(duration), 0)
        FROM study_sessions
    """)
    focus_minutes = cursor.fetchone()[0]

    # Tasks
    cursor.execute("""
        SELECT COUNT(*) FROM tasks
    """)
    total_tasks = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE completed = 1
    """)
    completed_tasks = cursor.fetchone()[0]

    # Goals
    cursor.execute("""
        SELECT COUNT(*) FROM goals
    """)
    total_goals = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM goals
        WHERE completed = 1
    """)
    completed_goals = cursor.fetchone()[0]

    # Best habit streak
    cursor.execute("""
        SELECT COALESCE(MAX(streak), 0)
        FROM habits
    """)
    best_streak = cursor.fetchone()[0]

    # Focus session history
    cursor.execute("""
        SELECT subject, duration, session_date
        FROM study_sessions
        ORDER BY id DESC
    """)
    sessions = cursor.fetchall()

    connection.close()

    return (
        focus_minutes,
        total_tasks,
        completed_tasks,
        total_goals,
        completed_goals,
        best_streak,
        sessions
    )


def render_progress():

    st.title("Progress")

    st.write(
        "Track your study activity and academic progress."
    )

    st.divider()

    (
        focus_minutes,
        total_tasks,
        completed_tasks,
        total_goals,
        completed_goals,
        best_streak,
        sessions
    ) = get_progress_data()

    # Main metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Focus Time",
            f"{focus_minutes} min"
        )

    with col2:

        if total_tasks > 0:
            task_rate = round(
                (completed_tasks / total_tasks) * 100
            )
        else:
            task_rate = 0

        st.metric(
            "Task Completion",
            f"{task_rate}%"
        )

    with col3:

        if total_goals > 0:
            goal_rate = round(
                (completed_goals / total_goals) * 100
            )
        else:
            goal_rate = 0

        st.metric(
            "Goal Completion",
            f"{goal_rate}%"
        )

    with col4:
        st.metric(
            "Best Habit Streak",
            f"{best_streak} days"
        )

    st.divider()

    # Completion overview
    st.subheader("Completion Overview")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.write("Tasks")

            st.write(
                f"{completed_tasks} of {total_tasks} tasks completed"
            )

            st.progress(
                task_rate / 100
            )

    with col2:

        with st.container(border=True):

            st.write("Study Goals")

            st.write(
                f"{completed_goals} of {total_goals} goals completed"
            )

            st.progress(
                goal_rate / 100
            )

    st.divider()

    # Focus history
    st.subheader("Focus Session History")

    if not sessions:

        st.info(
            "No focus sessions recorded yet."
        )

    else:

        for subject, duration, session_date in sessions:

            with st.container(border=True):

                col1, col2 = st.columns([4, 1])

                with col1:

                    st.write(subject)

                    st.caption(
                        f"Completed on {session_date}"
                    )

                with col2:

                    st.write(
                        f"{duration} min"
                    )