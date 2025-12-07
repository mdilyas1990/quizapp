from google import genai
import json
import streamlit as st

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("AI Quiz Generator & Evaluator")

topic = st.text_input("Give a topic")

if st.button("Generate Quiz"):

    prompt = f"""You are an expert in generating quiz questions.

    For the following topic - {topic}, generate 5 quiz questions in the following format.

     {{ "question":"text" ,
     "options": [A,B,C,D],
     "correct":"correct answer",
     "explanation":"short explanation"
     }}

    dont add anything before or after this."""

    response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = prompt,
            config={"response_mime_type":"application/json"}
            )

    data = json.loads(response.text)
    #st.write(data)
    st.session_state.quiz = data

if "quiz" in st.session_state:
    st.header("Quiz Questions")
    num = 1
    for ques in st.session_state.quiz:
        st.write(str(num) + ". " +  ques['question'])
        st.write(str(num) + ". " +  ques['correct'])
        st.radio("Choose:",ques['options'],key="chosen_answer"+str(num))

        num += 1

    if st.button("Submit"):
        st.header("Results")

        st.session_state.points = 0
        numb = 1
        for j in st.session_state.quiz:
            if j['correct'] == st.session_state['chosen_answer' +str(numb)]:
                st.session_state.points += 1
            numb += 1

        st.write(f"You have answered {st.session_state.points} questions correctly")

        st.header("Explanations")
        number = 1
        for j in st.session_state.quiz:
            st.write(str(number) + ") " + j['explanation'])
            number += 1
            
                
            
        




