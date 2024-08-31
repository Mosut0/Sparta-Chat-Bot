import glob
import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Union, Annotated

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.readers.json import JSONReader

app = FastAPI()
_ = load_dotenv(find_dotenv(), override=True)
UPLOAD_DIRECTORY = "./documents"
SYSTEM_PROMPT = """
You are a helpful assistant. Answer the user's question. If context is provided, you must answer based only on the 
context. If no context is provided, answer based on your knowledge. If you don't know the answer, say you don't know. 
Be concise. User query: 
"""

Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-large",
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base="REPLACE_WITH_YOUR",
)
Settings.llm = OpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base="REPLACE_WITH_YOUR",
)

json_files = glob.glob(os.path.join('./documents', '*.json'))

# Load data from all JSON files
documents = []
reader = JSONReader(levels_back=0)
for json_file in json_files:
    json_doc = reader.load_data(input_file=json_file, extra_info={})
    documents.extend(json_doc)
documents.extend(SimpleDirectoryReader(input_dir="./documents").load_data())
index = VectorStoreIndex.from_documents(documents)  # By default, data is stored in-memory.

@app.post("/user_query")
async def get_model_response(query: Annotated[str, Form()]):
    query_engine = index.as_query_engine(streaming=True, similarity_top_k=5)
    
    response_stream = query_engine.query(SYSTEM_PROMPT + query)
    return response_stream.get_response().response

@app.post("/add_document_file")
async def add_documentation(file: UploadFile = File(...)):
    global index
    # Add information to the document
    print(file.filename)
    if not file:
        raise HTTPException(status_code=400, detail="No upload file sent")
        
    # Ensure the upload directory exists
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
    
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    try:
        # Save the uploaded file asynchronously
        contents = file.file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        # Reload the documents and recreate the index
        documents = SimpleDirectoryReader("./documents").load_data()
        index = VectorStoreIndex.from_documents(documents)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Could not read file")
    
    return {"status": "success", "file_path": file_path}