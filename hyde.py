from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from util import LangType

class HyDEGenerator:
    def __init__(self, llm):
        self.llm = llm

    def _prepare_prompt(self, lang_type):
        parser = StrOutputParser()

        if lang_type == LangType.ZH.value:
            sys_prompt = "你是一个专业的技术文档助理。请根据用户的问题，生成一段300字左右、详细且正式的答案段落（不需要引用来源，直接写内容）。"
        else:
            sys_prompt = ("You are a professional technical documentation assistant. Please generate a detailed "
                          "and formal answer paragraph of approximately 300 words based on the user's question "
                          "(no need to cite sources, just write the content).")

        hyde_prompt = ChatPromptTemplate.from_messages([
            ("system", sys_prompt),
            ("human", "{question}")
        ])

        chain = hyde_prompt | self.llm | parser
        return chain

    def generate(self, question: str, lang_type) -> str:
        """输入问题，返回一段假想的答案文本"""
        try:
            chain = self._prepare_prompt(lang_type)
            hyde_doc = chain.invoke({"question": question})
            return hyde_doc.strip()
        except Exception as e:
            print(f"[HyDE] 生成失败，回退原始问题: {e}")
            return question  # 失败时降级为原始查询
