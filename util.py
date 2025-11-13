from pathlib import Path
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# if you in China you should set the HF_ENDPOINT, fuck the GreatWall. if you not in China, pls delete it.
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredPowerPointLoader,
    CSVLoader,
)

def load_document(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    elif ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    elif ext == ".pptx":
        loader = UnstructuredPowerPointLoader(file_path)
    elif ext == ".csv":
        loader = CSVLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    return loader.load()

def split_document(document):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )
    splits = splitter.split_documents(document)
    return splits

def embed_and_save(split_documents):
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
    vectorstore = Chroma.from_documents(
        documents=split_documents,
        embedding=embeddings,
        persist_directory="./chroma_db"  # 可选：保存到磁盘
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return retriever




# 批量加载 data/ 目录下所有支持的文件
for file in Path("/Users/coki/Desktop/教程/test").rglob("*.pdf"):
    print(file)
    docs = load_document(file)
    print(len(docs))
    splits = split_document(docs)
    print(len(splits))
    print(splits[0])
    retriever = embed_and_save(splits)
    result = retriever.invoke("Wikipedia")
    print(len(result))
    for d in result:
        print(d.page_content)
        print("================")