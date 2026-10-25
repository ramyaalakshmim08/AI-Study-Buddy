import streamlit as st
from database import get_connection


def add_goal(title, description, target_date):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO goals (title, description, target_date)
        VALUES (?, ?, ?)
        """,
        (title, description, str(target_date))
    )

    connection.commit()
    connection.close()


def get_goals():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, description, target_date, completed
        FROM goals
        ORDER BY completed, target_date
    """)

    goals = cursor.fetchall()
    connection.close()

    return goals


def update_goal(goal_id, completed):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE goals SET completed = ? WHERE id = ?",
        (completed, goal_id)
    )

    connection.commit()
    connection.close()


def render_goals():

    st.title("Study Goals")
    st.write("Set and track your academic goals.")

    st.divider()

    with st.form("add_goal_form"):
        st.subheader("Add a Study Goal")

        title = st.text_input("Goal title")
        description = st.text_area("Description")

        target_date = st.date_input("Target date")

        submitted = st.form_submit_button(
            "Add Goal",
            use_container_width=True
        )

        if submitted:
            if title.strip():
                add_goal(
                    title,
                    description,
                    target_date
                )

                st.success("Goal added successfully.")
                st.rerun()
            else:
                st.warning("Please enter a goal title.")

    st.divider()

    st.subheader("Your Goals")

    goals = get_goals()

    if not goals:
        st.info("No study goals yet. Add your first goal above.")
    else:
        for goal in goals:

            goal_id, title, description, target_date, completed = goal

            with st.container(border=True):

                if completed:
                    st.markdown(f"~~{title}~~")
                    st.caption(f"Completed • Target: {target_date}")
                else:
                    st.markdown(f"**{title}**")

                    if description:
                        st.caption(description)

                    st.caption(f"Target: {target_date}")

                    if st.button(
                        "Mark Complete",
                        key=f"complete_goal_{goal_id}"
                    ):
                        update_goal(goal_id, 1)
                        st.rerun()