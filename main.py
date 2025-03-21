import streamlit as st
import pandas as pd
import json


# Load questions from pasted JSON
def load_questions_from_json(text):
    try:
        data = json.loads(text)
        if "mcqs" not in data:
            st.error("JSON must contain a 'mcqs' key.")
            return None

        # Convert JSON to DataFrame
        questions = []
        for mcq in data["mcqs"]:
            question = mcq.get("question", "")
            options = mcq.get("options", {})
            answer = mcq.get("answer", "")
            questions.append(
                {
                    "Question": question,
                    "Option A": options.get("A", ""),
                    "Option B": options.get("B", ""),
                    "Option C": options.get("C", ""),
                    "Option D": options.get("D", ""),
                    "Answer": answer,
                }
            )
        return pd.DataFrame(questions)
    except Exception as e:
        st.error(f"Error parsing JSON: {e}")
        return None


# Main function
def main():
    st.title("MCQ Quiz App")
    st.write("Test your knowledge with multiple-choice questions!")

    # Text input for questions
    user_text = st.text_area("Paste your questions in JSON format:")

    if user_text:
        df = load_questions_from_json(user_text)
        if df is None:
            return

        st.write(f"Total Questions: {len(df)}")  # Show total number of questions

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
                f"JSON must contain the following fields: {', '.join(required_columns)}"
            )
            return

        if "question_index" not in st.session_state:
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.finished = False
            st.session_state.submitted = False

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

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("Submit", key=f"submit{st.session_state.question_index}"):
                    st.session_state.submitted = True
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

            with col2:
                if st.button(
                    "Next Question", key=f"next{st.session_state.question_index}"
                ):
                    if st.session_state.question_index < len(df) - 1:
                        st.session_state.question_index += 1
                        st.session_state.submitted = False

            with col3:
                if st.button(
                    "Previous Question", key=f"prev{st.session_state.question_index}"
                ):
                    if st.session_state.question_index > 0:
                        st.session_state.question_index -= 1
                        st.session_state.submitted = False

        if st.session_state.finished:
            st.success(
                f"Quiz Completed! Your Score: {st.session_state.score}/{len(df)}"
            )
            if st.button("Restart Quiz"):
                st.session_state.question_index = 0  # Reset index
                st.session_state.score = 0
                st.session_state.finished = False
                st.session_state.submitted = False


if __name__ == "__main__":
    main()
