<a name="top"></a>
* Other languages：[English](README.md), [中文](README_ch.md)。 

[![Free](https://img.shields.io/badge/free_for_non_commercial_use-brightgreen)](#-license)

⭐ If you think it's okay, please help give a star. 🙏😊

🔥 The purpose of this project is to create a local knowledge base (i.e., RAG) to unify the search of complex local documents. 
It does not require calling remote large models, completely offline, offline, offline. Important things are said three times.

## Table of Contents
- [Introduction](#-introduction)
- [Usage](#-usage)
- [Contact Information](#-contact-information)

## 🚀 introduction

This project is a RAG-type project developed based on LangChain, designed for quickly querying your local knowledge base. 
Currently, it supports document types: [".txt", ".pdf", ".docx", ".pptx", ".csv"]. In the future, 
support for images and other types of documents may be considered (if there are other needs, 
you can suggest them in the Issues section, and we can continue to optimize based on feedback).

## ✨ usage

- Double-click to run the 'app'(The first run will download the necessary large models from HuggingFace, which may be a bit slow)
- After it runs successfully, the page will show a message like 'Running on http://127.0.0.1:5000'
- Open a browser and enter: http://127.0.0.1:5000 to access the system
- After entering the file path, click Initialize
- Once initialization is complete, the corresponding document content will be converted into vector data and saved to the local vector database
- Initialization can be done multiple times (for example, including multiple file paths)
- If initialization is complete, there is no need to initialize the same path again; you can skip initialization and query directly

## 🗨️ contact-information

If you want to know more details, you can contact me by email.

- **Email**:  [xiao230coki@gmail.com](mailto:xiao230coki@gmail.com).
- **Issues**: You can leave a message in the project's Issues; I don't check emails often, but I check Issues frequently.

[Back to top](#top)