from dotenv import load_dotenv
import streamlit as st
from user_utils import *
import os

def main():
    load_dotenv()
    st.set_page_config(page_title="PerformanceX")
    st.title("PerformanceX")
    #st.header("A pioneering generative AI startup from Sweden, offers a unique Personal Co-Pilot for athletes. , our AI-driven platform helps athletes reduce stress and achieve their full potential. We prioritize data security and ensure our users' information is protected with robust security measures", divider="blue")
    st.subheader("A pioneering generative AI startup from Sweden, offers a unique Personal Co-Pilot for athletes", divider=True)
    
    multi = '''
    <p style="text-align: justify;">
    Combining personalized coaching, 
    psychological support, and performance optimization, our AI-driven platform helps athletes reduce stress and achieve their full potential. 
    We prioritize data security and ensure our users' information is protected with robust security measures.
    </p>
    '''

    st.markdown(multi, unsafe_allow_html=True)
    
    questions = '''
    <h4 style="text-align: justify;">Here are three engaging questions to kick off a conversation with our Personal Sports Coach:</h3>
    <ol style="text-align: justify;">
        <li>What's your biggest challenge in your sport right now?</li>
        <li>How do you typically prepare mentally before a big game or competition?</li>
        <li>What aspect of your training or performance do you wish you had more support with?</li>
    </ol>
    '''

    st.markdown(questions, unsafe_allow_html=True)


    st.sidebar.image("https://dcassetcdn.com/design_img/4077411/1363205/33612364/n1fphb57h65khkmdxps3m2h6b3_image.png")

    embeddings = create_embeddings()
    pinecone_key = st.secrets['PINECONE_API_KEY']
    index = pull_from_pinecone(pinecone_key, "us-east-1", "performancex", embeddings)

    if "history" not in st.session_state:
        st.session_state["history"] = []

    user_input = st.chat_input("How can PerformanceX help you today?")

    if user_input:
        st.session_state["history"].append({"role": "user", "content": user_input})

        with st.spinner("I am working on it"):
            relevant_docs = get_similar_docs(index, user_input)
            if relevant_docs and is_relevant(relevant_docs[0], user_input):
                response = get_answer(relevant_docs, user_input)
            else:
                response = get_llm_answer(user_input)

        st.session_state["history"].append({"role": "assistant", "content": response})

    for message in st.session_state["history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if __name__ == '__main__':
    main()
