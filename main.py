import streamlit as st
import pandas as pd
import io


# Load questions from pasted text
def load_questions_from_text(text):
    try:
        df = pd.read_csv(io.StringIO(text))
        return df
    except Exception as e:
        st.error(f"Error parsing text: {e}")
        return None


# Main function
def main():
    st.title("MCQ Quiz App")
    st.write("Test your knowledge with multiple-choice questions!")

    # Text input for questions
    user_text = st.text_area("Paste your questions in CSV format:")

    if user_text:
        df = load_questions_from_text(user_text)
        if df is None:
            return

        required_columns = [
            "Question",
            "Option A",
            "Option B",
            "Option C",
            "Option D",
            "Answer",
        ]
        if not all(col in df.columns for col in required_columns):
            st.error(
                f"CSV text must contain the following columns: {', '.join(required_columns)}"
            )
            return

        if "question_index" not in st.session_state:
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.finished = False

        if st.session_state.question_index < len(df):
            row = df.iloc[st.session_state.question_index]
            question = row["Question"]
            options = [
                row["Option A"],
                row["Option B"],
                row["Option C"],
                row["Option D"],
            ]
            correct_answer = str(row["Answer"]).strip().upper()

            st.subheader(f"Q{st.session_state.question_index + 1}: {question}")
            user_answer = st.radio(
                "Select an option:", options, key=f"q{st.session_state.question_index}"
            )

            if st.button("Submit", key=f"submit{st.session_state.question_index}"):
                if (
                    correct_answer in ["A", "B", "C", "D"]
                    and user_answer == options[ord(correct_answer) - ord("A")]
                ):
                    st.success("Correct!")
                    st.session_state.score += 1
                else:
                    st.error(
                        f"Wrong! Correct answer: {options[ord(correct_answer) - ord('A')]}"
                    )

                st.session_state.question_index += 1

                if st.session_state.question_index >= len(df):
                    st.session_state.finished = True

        if st.session_state.finished:
            st.success(
                f"Quiz Completed! Your Score: {st.session_state.score}/{len(df)}"
            )
            if st.button("Restart Quiz"):
                st.session_state.question_index = 0  # Reset index
                st.session_state.score = 0
                st.session_state.finished = False


if __name__ == "__main__":
    main()
