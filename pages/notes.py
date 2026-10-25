import streamlit as st
from database import get_connection


def add_note(title, content, folder):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO notes (title, content, folder, created_at)
        VALUES (?, ?, ?, datetime('now'))
        """,
        (title, content, folder)
    )

    connection.commit()
    connection.close()


def get_notes():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, content, folder, created_at
        FROM notes
        ORDER BY id DESC
    """)

    notes = cursor.fetchall()
    connection.close()

    return notes


def get_folders():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT folder
        FROM notes
        WHERE folder IS NOT NULL AND folder != ''
        ORDER BY folder
    """)

    folders = [row[0] for row in cursor.fetchall()]

    connection.close()

    return folders


def render_notes():

    st.title("Notes & Folders")
    st.write("Create, organize, and manage your study notes.")

    st.divider()

    folders = get_folders()

    st.subheader("Create a Note")

    with st.form("add_note_form"):

        title = st.text_input("Note title")

        folder_options = ["General"] + folders

        folder_choice = st.selectbox(
            "Folder",
            folder_options
        )

        custom_folder = st.text_input(
            "New folder (optional)",
            placeholder="Example: Java, OS, Data Structures"
        )

        content = st.text_area(
            "Note content",
            height=200
        )

        submitted = st.form_submit_button(
            "Save Note",
            use_container_width=True
        )

        if submitted:

            if not title.strip() or not content.strip():

                st.warning(
                    "Please enter both a title and note content."
                )

            else:

                folder = (
                    custom_folder.strip()
                    if custom_folder.strip()
                    else folder_choice
                )

                add_note(
                    title.strip(),
                    content.strip(),
                    folder
                )

                st.success("Note saved successfully.")
                st.rerun()

    st.divider()

    st.subheader("Your Notes")

    notes = get_notes()

    if not notes:

        st.info(
            "No notes yet. Create your first study note above."
        )

        return

    filter_options = ["All Folders"] + sorted(
        set(note[3] for note in notes)
    )

    selected_folder = st.selectbox(
        "Filter by folder",
        filter_options
    )

    if selected_folder == "All Folders":

        filtered_notes = notes

    else:

        filtered_notes = [
            note for note in notes
            if note[3] == selected_folder
        ]

    if not filtered_notes:

        st.info("No notes found in this folder.")

    else:

        for note in filtered_notes:

            note_id, title, content, folder, created_at = note

            with st.container(border=True):

                st.markdown(f"**{title}**")

                st.caption(
                    f"Folder: {folder} • Created: {created_at}"
                )

                st.write(content)