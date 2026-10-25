import streamlit as st

from services.retriever import retrieve_context
from services.llm import generate_answer


def render_assistant():

    st.title("AI Study Assistant")
    st.write(
        "Ask questions, understand concepts, and study from your own materials."
    )

    st.divider()

    study_mode = st.selectbox(
        "Study Mode",
        [
            "Ask a Question",
            "Explain a Concept",
            "Summarize",
            "Exam Answer",
            "Generate Quiz"
        ]
    )

    question = st.text_area(
        "What would you like to study?",
        placeholder="Example: Explain inheritance in Java with a simple example.",
        height=120
    )

    if st.button(
        "Generate Response",
        use_container_width=True
    ):

        if not question.strip():

            st.warning("Please enter a question or topic.")
            return

        with st.spinner("Studying your materials..."):

            context_documents = retrieve_context(question)

            if not context_documents:

                st.warning(
                    "No relevant study material was found."
                )
                return

            context = "\n\n".join(context_documents)

            try:

                answer = generate_answer(
                    question,
                    context,
                    study_mode
                )

                st.subheader("AI Study Response")
                st.write(answer)

            except Exception as error:

                st.error(
                    f"Unable to generate the AI response: {error}"
                )