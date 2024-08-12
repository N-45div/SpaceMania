import os
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("spacemania-ffc62-fc83d367ab53.json")  # Update with your Firebase credentials file path
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

if not GOOGLE_API_KEY:
    st.error("Google API key is not set in the environment variables.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

def signup(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        st.success("User created successfully! Please log in.")
    except Exception as e:
        st.error(f"Error signing up: {e}")

def login(email, password):
    try:
        user = auth.get_user_by_email(email)
        # For demonstration, we assume successful login if the user exists
        # In a real app, you should validate the password on the client-side
        return user
    except Exception as e:
        st.error(f"Error logging in: {e}")
        return None

def get_pdf_text(pdf_docs):
    try:
        text = ""
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def get_text_chunks(text):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        chunks = text_splitter.split_text(text)
        return chunks
    except Exception as e:
        st.error(f"Error splitting text: {e}")
        return []

def get_vector_store(text_chunks):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
    except Exception as e:
        st.error(f"Error creating vector store: {e}")

def get_conversational_chain():
    try:
        prompt_template = """
        Answer the question as detailed as possible from the provided context. If the answer is not in the provided context, 
        just say, "answer is not available in the context", don't provide a wrong answer.\n\n
        Context:\n {context}\n
        Question: \n{question}\n
        Answer:
        """
        
        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
        
        return chain
    except Exception as e:
        st.error(f"Error creating conversational chain: {e}")
        return None

def store_response(user_id, question, response):
    try:
        db.collection("responses").add({
            "user_id": user_id,
            "question": question,
            "response": response,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
    except Exception as e:
        st.error(f"Error storing response: {e}")

def user_input(user_question, user_id):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)

        chain = get_conversational_chain()
        if chain:
            response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
            st.write("Reply: ", response["output_text"])

            # Store the response in Firestore
            store_response(user_id, user_question, response["output_text"])
    except Exception as e:
        st.error(f"Error processing user input: {e}")

def main():
    st.set_page_config(page_title="Spacemania", page_icon="🚀")

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.title("Welcome to Spacemania 🚀")
        st.write("An innovative tool to interact with your PDFs using advanced AI technology.")

        # Sign-Up
        signup_email = st.text_input("Sign Up - Email")
        signup_password = st.text_input("Sign Up - Password", type="password")
        if st.button("Sign Up"):
            if signup_email and signup_password:
                signup(signup_email, signup_password)
            else:
                st.error("Please enter both email and password to sign up.")

        st.write("----")

        # Login
        login_email = st.text_input("Login - Email")
        login_password = st.text_input("Login - Password", type="password")
        if st.button("Login"):
            if login_email and login_password:
                user = login(login_email, login_password)
                if user:
                    st.session_state['user'] = user
                    st.session_state['logged_in'] = True
                    # Clear the input fields
                    st.text_input("Login - Email", value="", key="login_email")
                    st.text_input("Login - Password", value="", type="password", key="login_password")
                else:
                    st.error("Invalid email or password.")
            else:
                st.error("Please enter both email and password to login.")
    else:
        user_id = st.session_state['user'].uid
        st.sidebar.write("You are logged in as:", st.session_state['user'].email)
        st.sidebar.write("Welcome to Spacemania! Start interacting with your PDFs below.")

        st.header("Chat with PDF")
        user_question = st.text_input("Ask a Question from the PDF Files")

        if user_question:
            user_input(user_question, user_id)

        st.write("----")

        with st.sidebar:
            st.title("Menu:")
            pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
            if st.button("Submit & Process"):
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    if raw_text:
                        text_chunks = get_text_chunks(raw_text)
                        if text_chunks:
                            get_vector_store(text_chunks)
                            st.success("Processing complete.")
                        else:
                            st.error("Error during text chunking.")
                    else:
                        st.error("Error during PDF text extraction.")

if __name__ == "__main__":
    main()
