import streamlit as st
from database import get_connection


def add_task(title, description, due_date, priority):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, description, due_date, priority)
        VALUES (?, ?, ?, ?)
        """,
        (title, description, due_date, priority)
    )

    connection.commit()
    connection.close()


def get_tasks():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, description, due_date, priority, completed
        FROM tasks
        ORDER BY completed, due_date
    """)

    tasks = cursor.fetchall()
    connection.close()

    return tasks


def update_task(task_id, completed):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE tasks SET completed = ? WHERE id = ?",
        (completed, task_id)
    )

    connection.commit()
    connection.close()


def render_tasks():

    st.title("Tasks")
    st.write("Manage assignments, study tasks, and deadlines.")

    st.divider()

    with st.form("add_task_form"):
        st.subheader("Add a Task")

        title = st.text_input("Task title")
        description = st.text_area("Description")

        col1, col2 = st.columns(2)

        with col1:
            due_date = st.date_input("Due date")

        with col2:
            priority = st.selectbox(
                "Priority",
                ["Low", "Medium", "High"]
            )

        submitted = st.form_submit_button(
            "Add Task",
            use_container_width=True
        )

        if submitted:
            if title.strip():
                add_task(
                    title,
                    description,
                    str(due_date),
                    priority
                )

                st.success("Task added successfully.")
                st.rerun()
            else:
                st.warning("Please enter a task title.")

    st.divider()

    st.subheader("Your Tasks")

    tasks = get_tasks()

    if not tasks:
        st.info("No tasks yet. Add your first task above.")
    else:
        for task in tasks:
            task_id, title, description, due_date, priority, completed = task

            with st.container(border=True):

                col1, col2 = st.columns([5, 1])

                with col1:
                    if completed:
                        st.markdown(f"~~{title}~~")
                    else:
                        st.markdown(f"**{title}**")

                    if description:
                        st.caption(description)

                    st.caption(
                        f"Due: {due_date}  •  Priority: {priority}"
                    )

                with col2:
                    if not completed:
                        if st.button(
                            "Complete",
                            key=f"complete_{task_id}"
                        ):
                            update_task(task_id, 1)
                            st.rerun()