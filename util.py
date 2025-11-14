from pathlib import Path
import os
# if you in China you should set the HF_ENDPOINT, fuck the GreatWall. if you not in China, pls delete it.
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_CONCURRENT_DOWNLOADS"] = "3"

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
chroma_db_path = "./chroma_db"

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
    if not os.path.exists(chroma_db_path):
        vectorstore = Chroma.from_documents(
            documents=split_documents,
            embedding=embeddings,
            persist_directory=chroma_db_path  # 可选：保存到磁盘
        )
    else:
        vectorstore = Chroma.from_documents(
            documents=split_documents,
            embedding=embeddings,
        )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return retriever

def get_llm():
    model_id = "Qwen/Qwen2-1.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",  # 自动分配 GPU/CPU
        trust_remote_code=True,
        # 可选：量化降低显存（适合低配设备）
        # load_in_4bit=True,
    )
    # 创建文本生成 pipeline
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.2,
        top_k=50,
        return_full_text=False,  # 只返回生成内容
    )
    llm = HuggingFacePipeline(pipeline=pipe)
    return llm

def query(question, q_retriever):
    llm = get_llm()

    # 自定义提示模板
    template = """根据以下上下文回答问题：
    {context}

    问题: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # 构建 RAG 链
    rag_chain = (
            {"context": q_retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )
    response = rag_chain.invoke(question)
    print(response)


# 批量加载 data/ 目录下所有支持的文件
for file in Path("/Users/coki/Desktop/教程/test").rglob("*.pdf"):
    print(file)
    docs = load_document(file)
    print(len(docs))
    splits = split_document(docs)
    print(len(splits))
    print(splits[0])
    retriever = embed_and_save(splits)
    result = query("what is Stack Exchange? ",retriever)
    print(result)