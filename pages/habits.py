import streamlit as st
from database import get_connection
from datetime import date


def add_habit(name, frequency):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO habits (name, frequency, streak, last_completed)
        VALUES (?, ?, ?, ?)
        """,
        (name, frequency, 0, None)
    )

    connection.commit()
    connection.close()


def get_habits():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, frequency, streak, last_completed
        FROM habits
        ORDER BY id DESC
    """)

    habits = cursor.fetchall()

    connection.close()

    return habits


def complete_habit(habit_id, streak, last_completed):

    today = str(date.today())

    if last_completed == today:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE habits
        SET streak = ?, last_completed = ?
        WHERE id = ?
        """,
        (streak + 1, today, habit_id)
    )

    connection.commit()
    connection.close()

    return True


def render_habits():

    st.title("Habits")
    st.write(
        "Build consistent study habits and track your progress."
    )

    st.divider()

    with st.form("add_habit_form"):

        st.subheader("Add a Study Habit")

        name = st.text_input(
            "Habit name",
            placeholder="Example: Practice Java for 30 minutes"
        )

        frequency = st.selectbox(
            "Frequency",
            ["Daily", "Weekly"]
        )

        submitted = st.form_submit_button(
            "Add Habit",
            use_container_width=True
        )

        if submitted:

            if name.strip():

                add_habit(
                    name.strip(),
                    frequency
                )

                st.success("Habit added successfully.")
                st.rerun()

            else:

                st.warning("Please enter a habit name.")

    st.divider()

    st.subheader("Your Habits")

    habits = get_habits()

    if not habits:

        st.info(
            "No habits yet. Add your first study habit above."
        )

        return

    for habit in habits:

        habit_id, name, frequency, streak, last_completed = habit

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.markdown(f"**{name}**")

                st.caption(
                    f"{frequency} • Current streak: {streak} days"
                )

            with col2:

                if st.button(
                    "Complete",
                    key=f"habit_{habit_id}"
                ):

                    completed = complete_habit(
                        habit_id,
                        streak,
                        last_completed
                    )

                    if completed:
                        st.rerun()

                    else:
                        st.info("Already completed today.")