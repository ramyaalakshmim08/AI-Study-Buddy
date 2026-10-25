import streamlit as st
import os

from services.pdf_reader import extract_text_from_pdf


MATERIALS_FOLDER = "data/materials"


def render_materials():

    st.title("My Materials")
    st.write("Upload and manage your study materials.")

    st.divider()

    os.makedirs(MATERIALS_FOLDER, exist_ok=True)

    st.subheader("Upload Study Material")

    uploaded_file = st.file_uploader(
        "Choose a PDF or text file",
        type=["pdf", "txt"]
    )

    if uploaded_file is not None:

        file_path = os.path.join(
            MATERIALS_FOLDER,
            uploaded_file.name
        )

        with open(file_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        st.success(
            f"{uploaded_file.name} uploaded successfully."
        )

        if uploaded_file.name.lower().endswith(".pdf"):

            try:
                extracted_text = extract_text_from_pdf(file_path)

                st.subheader("Extracted Text")

                if extracted_text.strip():

                    st.text_area(
                        "PDF content",
                        extracted_text,
                        height=300
                    )

                else:

                    st.warning(
                        "No readable text was found in this PDF."
                    )

            except Exception as error:

                st.error(
                    f"Could not read the PDF: {error}"
                )

    st.divider()

    st.subheader("Your Materials")

    files = os.listdir(MATERIALS_FOLDER)

    if not files:

        st.info("No study materials uploaded yet.")

    else:

        for file_name in sorted(files):

            with st.container(border=True):

                st.write(file_name)

                if file_name.lower().endswith(".pdf"):
                    st.caption("PDF document")

                elif file_name.lower().endswith(".txt"):
                    st.caption("Text document")