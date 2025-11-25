from pathlib import Path
import os
from enum import Enum
from hyde import HyDEGenerator

# if you in China you should set the HF_ENDPOINT, fuck the GreatWall. if you not in China, pls delete it.
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_CONCURRENT_DOWNLOADS"] = "3"

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline, HuggingFaceEmbeddings
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

class FileType(Enum):
    TXT = ".txt"
    PDF = ".pdf"
    DOCX = ".docx"
    PPTX = ".pptx"
    CSV = ".csv"

class LangType(Enum):
    EN = "en"
    ZH = "zh"

def get_embedding_model(lang_type):
    if lang_type == LangType.ZH.value:
        return HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
    else:
        return HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

def load_document(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == FileType.TXT.value:
        loader = TextLoader(file_path, encoding="utf-8")
    elif ext == FileType.PDF.value:
        loader = PyPDFLoader(file_path)
    elif ext == FileType.DOCX.value:
        loader = Docx2txtLoader(file_path)
    elif ext == FileType.PPTX.value:
        loader = UnstructuredPowerPointLoader(file_path)
    elif ext == FileType.CSV.value:
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

def embed_and_save(split_documents, embeddings, lang_type):
    # diff language use diff vector
    c_path = get_db_path(lang_type)
    if not os.path.exists(c_path):
        vectorstore = Chroma.from_documents(
            documents=split_documents,
            embedding=embeddings,
            persist_directory=c_path  # 可选：保存到磁盘
        )
    else:
        # 加载已有数据库
        vectorstore = Chroma(persist_directory=c_path, embedding_function=embeddings)
        vectorstore.add_documents(documents=split_documents)

    vectorstore.persist()

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

def query(question, q_retriever, lang_type):
    llm = get_llm()
    hyde = HyDEGenerator(llm)
    hyde_prompt = hyde.generate(question, lang_type)


    # 自定义提示模板
    if lang_type == "en":
        template = """Answer the questions based on the following context, If there is a gap between the context and reality, 
        provide the answer according to the context first, 
        and then supplement with the differences from reality.：
        {context}

        Question: {question}
        """
    else:
        template = """根据以下上下文回答问题，答案以上下文为主，如果上下文和实际有出入，先给出上下文的答案，后在补充和实际的差异：
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
    response = rag_chain.invoke(hyde_prompt)
    return response

def get_all_files(directory):
    folder = Path(directory)
    extensions = [file_type.value for file_type in FileType]# 想要的文件类型
    files = [f for f in folder.rglob('*') if f.is_file() and f.suffix.lower() in extensions]
    return files

def parse_file(file_path, embeddings, lang_type):
    documents = load_document(file_path)
    splits = split_document(documents)
    embed_and_save(splits, embeddings, lang_type)

def get_db_path(lang_type):
    # diff language use diff vector
    c_path = chroma_db_path + "_" + lang_type
    return c_path

def get_retriever(embeddings, lang_type):
    c_path = get_db_path(lang_type)
    if not os.path.exists(c_path):
        raise ValueError("cannot find chroma db")
    else:
        vectorstore = Chroma(persist_directory=c_path, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return retriever

# def classify_language(text):
#     if not text:
#         return "empty"
#
#     # 统计中文和英文字母的数量
#     chinese_count = 0
#     english_count = 0
#
#     for char in text:
#         code = ord(char)
#         # 判断是否为中文字符（常见汉字范围）
#         if 0x4e00 <= code <= 0x9fff:
#             chinese_count += 1
#         # 判断是否为英文字母
#         elif 65 <= code <= 90 or 97 <= code <= 122:  # A-Z 或 a-z
#             english_count += 1
#
#     total_letters = chinese_count + english_count
#
#     if total_letters == 0:
#         return "other"  # 比如全是数字、标点等
#
#     # 判断主体语言
#     if chinese_count < english_count:
#         return "en"
#     else:
#         return "zh"

def init_embedding(directory, lang_type):
    all_file = get_all_files(directory)
    for file in all_file:
        parse_file(file, get_embedding_model(lang_type), lang_type)

def retrieve_language(text, lang_type):
    # lang_type = classify_language(text)
    embedding_model = get_embedding_model(lang_type)
    return query(text, get_retriever(embedding_model, lang_type), lang_type)



