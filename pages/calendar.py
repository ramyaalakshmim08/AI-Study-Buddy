import streamlit as st
from database import get_connection


def add_event(title, event_date, event_time, description):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO calendar_events
        (title, event_date, event_time, description)
        VALUES (?, ?, ?, ?)
        """,
        (
            title,
            str(event_date),
            event_time,
            description
        )
    )

    connection.commit()
    connection.close()


def get_events():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, event_date, event_time, description
        FROM calendar_events
        ORDER BY event_date, event_time
    """)

    events = cursor.fetchall()

    connection.close()

    return events


def render_calendar():

    st.title("Calendar")
    st.write(
        "Plan exams, deadlines, study sessions, and important academic events."
    )

    st.divider()

    with st.form("add_event_form"):

        st.subheader("Add an Event")

        title = st.text_input(
            "Event title",
            placeholder="Example: Java Internal Exam"
        )

        col1, col2 = st.columns(2)

        with col1:
            event_date = st.date_input("Date")

        with col2:
            event_time = st.time_input("Time")

        description = st.text_area(
            "Description",
            placeholder="Add any important details..."
        )

        submitted = st.form_submit_button(
            "Add Event",
            use_container_width=True
        )

        if submitted:

            if title.strip():

                add_event(
                    title.strip(),
                    event_date,
                    str(event_time),
                    description.strip()
                )

                st.success("Event added successfully.")
                st.rerun()

            else:

                st.warning("Please enter an event title.")

    st.divider()

    st.subheader("Upcoming Events")

    events = get_events()

    if not events:

        st.info("No calendar events yet.")

        return

    for event in events:

        event_id, title, event_date, event_time, description = event

        with st.container(border=True):

            st.markdown(f"**{title}**")

            st.caption(
                f"{event_date} • {event_time}"
            )

            if description:

                st.write(description)