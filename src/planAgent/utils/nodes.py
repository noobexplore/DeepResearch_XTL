#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Author: GODTAO
@Contact: taoling.xu@transwarp.io
@File: node.py
@Time: 2025/6/25 19:08
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.types import interrupt
from src.planAgent.utils.prompt import system_prompt
from src.planAgent.utils.state import CodeState, codeContent
from src.planAgent.utils.tools import safe_python_repl
from src.planAgent.configure import Configuration
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.fix import OutputFixingParser
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()  # 这里通过环境变量配置相应的apikey

if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY is not set")
else:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if os.getenv("OPENAI_API_URL") is None:
    raise ValueError("OPENAI_API_URL is not set")
else:
    OPENAI_API_URL = os.getenv("OPENAI_API_URL")

if os.getenv("LANGSMITH_API_KEY") is None:
    raise ValueError("LANGSMITH_API_KEY is not set")
else:
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")


def call_model(state: CodeState, config: RunnableConfig):
    configurable = Configuration.from_runnable_config(config)
    llm = ChatOpenAI(
        model=configurable.coder_model,
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=OPENAI_API_URL,
        temperature=configurable.temperature,
        max_tokens=configurable.max_tokens,
        request_timeout=100,
        extra_body={"enable_thinking": configurable.enable_thinking}
    )
    parser = PydanticOutputParser(pydantic_object=codeContent)  # 定义你的原始解析器
    output_fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
    prompt = ChatPromptTemplate.from_messages([
        system_prompt,
        ("user", "{input}")
    ])
    chain = prompt | llm | output_fixing_parser
    feed_dict = {
        "sample_data_input": state["sample_data_input"],
        "sample_data_output": state["sample_data_output"],
        "data_logical": state["data_logical"],
        "input": state["messages"][0].content
    }
    response = chain.invoke(input=feed_dict)
    return {"command_txt": response.code_str}


def feedback_generate(state: CodeState):
    """这里将生成的code展示给前端"""
    feedback_command_res = interrupt({"command_txt": state["command_txt"]})
    return {"command_txt": feedback_command_res["code"]}


def execute_python(state: CodeState):
    code_res = safe_python_repl(state["command_txt"])
    return {"code_res": code_res}
