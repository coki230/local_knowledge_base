<a name="top"></a>
* Other languages：[English](README.md), [中文](README_zh.md)。 
[![Free](https://img.shields.io/badge/free_for_non_commercial_use-brightgreen)](#-license)

⭐ 如果觉得还行，请帮忙打星 🙏😊

🔥 这个项目的目的是为了统一查询本地繁杂的文档而做的一个本地知识库（也就是RAG），不需要调用远程大模型，完全离线，离线，离线。
重要的事情说三遍。

## Table of Contents
- [简介](#-简介)
- [使用方法](#-使用方法)
- [联系方法](#-联系方法)

## 🚀 简介

此项目基于langchain开发的RAG类型的项目，用来快速查询自己本地的知识库，目前支持文档类型为：[".txt", ".pdf", ".docx", ".pptx", ".csv"]。
后期可以考虑加入图片和其他类型的文档（如果有其他需求可以在Issues里面提，根据大家的反馈可以继续优化。）

## ✨ 使用方法

- 双击运行“app”（第一次运行会去HuggingFace下载必须的大模型，可能会比较慢）
- 运行成功后页面会有类似“Running on http://127.0.0.1:5000”的提示
- 打开浏览器输入：http://127.0.0.1:5000。进入系统
- 输入文件路径后，点击初始化
- 初始化完成后会把对应的文档内容转为向量数据保存到本地的向量数据库
- 可以多次初始化（比如包含多个文件路径）
- 如果初始化完成后，不需要再次初始化相同的路径，跳过初始化可以直接查询

## 🗨️ 联系方法

如果希望更详细的了解，可以邮件联系我

- **Email**:  [xiao230coki@gmail.com](mailto:xiao230coki@gmail.com).
- **Issues**: 可以在项目里的Issues里留言，邮件不经常看，Issues会经常看

[Back to top](#top)