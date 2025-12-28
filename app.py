import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

#seting the page title
st.set_page_config(page_title="Study Partner", page_icon="🎓")

#load the key from env
load_dotenv()

#check for the key
if not os.getenv("OPENAI_API_KEY"):
    st.error("OpenAI API Key is missing")
    st.info("the key is missing or not right")
    st.stop()

# --- Logic: Processing the Files ---
def process_documents(uploaded_files):
    all_docs = []
    # Save files locally temporarily to load them
    if not os.path.exists("temp"): os.makedirs("temp")

    for uploaded_file in uploaded_files:
        temp_path = f"temp/{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        loader = PyPDFLoader(temp_path)
        all_docs.extend(loader.load())

    # Chunking:  using RecursiveCharacterTextSplitter for better context preservation
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(all_docs)

    # Vector Store
    embeddings = OpenAIEmbeddings()#embeddings the files conntent using openAI
    #using the facebook vector database
    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore


# --- Logic: Creating the RAG Chain ---
def get_rag_chain(vectorstore):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Define how the AI should behave (System Prompt)
    system_prompt = (
        "You are an expert tutor. Use the following pieces of retrieved context "
        "to answer the question. If you don't know the answer, say you don't know. "
        "to make a quiz. use MCQ type of quiz, provide four answers maximum"
        "Use five sentences maximum and keep the answer concise.\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(vectorstore.as_retriever(), question_answer_chain)


# --- UI: Sidebar & State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

with st.sidebar:
    #seting the title
    st.title("📚 Study Knowledge")
    #the type of accepted files (here we accept mul of pdf only)
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    #start the studing of the file (embedding,etc...)
    if st.button("Index Documents") and files:
        with st.spinner("Analyzing your textbooks..."):
            vs = process_documents(files)
            st.session_state.rag_chain = get_rag_chain(vs)
            st.success("Ready to study!")

# --- UI: Chat Window ---
st.title("AI Study Assistant")
#going through the masseges
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a question about your files..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    #if the file is uploaded correctly we normaly continue
    if st.session_state.rag_chain:
        with st.chat_message("assistant"):
            # Standard LangChain invocation
            response = st.session_state.rag_chain.invoke({"input": prompt})
            answer = response["answer"]
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
    #the file is not uploaded correctly or not uploaded at all
    else:
        st.info("Please upload and index your documents first.")