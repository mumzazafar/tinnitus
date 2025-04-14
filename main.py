import os
from fastapi import FastAPI,status,HTTPException
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain.prompts import PromptTemplate # for giving the instructions about LLm.
from langchain_groq import ChatGroq # Chat groq is free LLM like chatgpt


# Set Groq API Key (Replace with your own)
os.environ["GROQ_API_KEY"] = "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"

app = FastAPI()

# Hardcoded file path
FILE_PATH = "SereniTinnitusApp-3012words.docx"

# Load Word Document
def load_word_doc(filepath: str):
    loader = UnstructuredWordDocumentLoader(filepath)
    documents = loader.load()
    return " ".join([doc.page_content for doc in documents])

# Load document at startup
document_text = load_word_doc(FILE_PATH)
print(document_text[:500])

# Define a Prompt Template (Instrcutions for LLM)
prompt_template = PromptTemplate(
    input_variables=["context", "query"],
    template = (
    "You are TinniAI, an AI assistant specialized in providing expert answers about Tinnitus, "
    "a medical condition affecting the ears. Your responses should be accurate, concise, and "
    "relevant to Tinnitus. Avoid saying things like 'The name of the app is not explicitly mentioned in the document.' "
    "Instead, provide a helpful response based on the given document.\n\n"
    "Refer to the following document content:\n\n"
    "{context}\n\n"
    "Now, answer the following question clearly and concisely:\n\n{query}"
)
)

# Ask question based on the document
@app.get("/ask")
async def ask_question(query: str):
    if not document_text:
        return {"error": "Document could not be loaded"}

    # Format prompt with document content
    formatted_prompt = prompt_template.format(context=document_text, query=query)

    # Generate response using Groq
    llm = ChatGroq(model="llama-3.1-8b-instant")
    response = llm.invoke(formatted_prompt)
    content = response.content

    return {"answer": content}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)