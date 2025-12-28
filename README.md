# Study Partner 🎓
### **AI Study Assistant**

**Study Partner** is a Streamlit-based application designed to help students and researchers interact with their textbooks. By leveraging **RAG (Retrieval-Augmented Generation)**, the app allows users to upload multiple PDF documents, index them, and then ask questions or generate quizzes based on the content.



## ✨ Key Features
* **PDF Document Indexing 📄**: Upload and process multiple PDF files simultaneously using `PyPDFLoader`.
* **Semantic Search & Retrieval 🔍**: Uses **FAISS** (Facebook AI Similarity Search) and **OpenAI Embeddings** to find the most relevant context for your questions.
* **Smart Study Assistant 🧠**: Powered by `gpt-4o-mini`, the assistant provides concise answers and can even generate **MCQ-style quizzes** from your material.
* **Context Preservation 🧩**: Implements `RecursiveCharacterTextSplitter` to ensure text chunks maintain meaningful context during the embedding process.

## 🛠️ Tech Stack
* **Frontend**: [Streamlit](https://streamlit.io/)
* **LLM Framework**: [LangChain](https://www.langchain.com/)
* **Model**: OpenAI `gpt-4o-mini`
* **Vector Database**: FAISS
* **Environment Management**: `python-dotenv`

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed and an **OpenAI API Key**.

### 2. Installation
Clone this repository and install the required dependencies:
```bash
pip install streamlit langchain langchain-openai langchain-community faiss-cpu pypdf python-dotenv
