#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Author: GODTAO
@Contact: taoling.xu@transwarp.io
@File: configure.py
@Time: 2025/7/28 11:08
"""
import os
from langgraph.types import Command
from langgraph.graph import StateGraph, END
from src.planAgent.api.model import CoderRequest
from src.planAgent.utils.state import CodeState
from src.planAgent.configure import Configuration
from langgraph.checkpoint.postgres import PostgresSaver
from src.planAgent.utils.nodes import call_model, execute_python, feedback_generate

if os.getenv("POSTGRES_URI") is None:
    raise ValueError("POSTGRES_URI is not set")
else:
    POSTGRES_URI = os.getenv("POSTGRES_URI")

workflow = StateGraph(CodeState, config_schema=Configuration)
workflow.add_node("agent", call_model)
workflow.add_node("exec", execute_python)
workflow.add_node("feed", feedback_generate)  # 加入代码审查机制
workflow.set_entry_point("agent")
workflow.add_edge("agent", "feed")
workflow.add_edge("feed", "exec")
workflow.add_edge("exec", END)
graph = workflow.compile(name="code master")


def response_process(response):
    res_msg = {}
    if "__interrupt__" in response:
        res_msg["messages"] = "中断需要人类介入"
        res_msg["params"] = response["__interrupt__"][-1].value
    else:
        res_msg["messages"] = response["messages"]
    return res_msg


def coder_master_sync(codeRequest: CoderRequest):
    """代码大师同步生成接口"""
    # checkpointer = MemorySaver()  # 这个一定是全局共享的
    config = {"configurable": {"thread_id": codeRequest.agent_meta.thread_id}}
    input_message = {
        "messages": [("human", f"{codeRequest.input_data}")],
        "sample_data_input": codeRequest.sample_data_input,
        "sample_data_output": codeRequest.sample_data_output,
        "data_logical": codeRequest.data_logical
    }
    # 初始化checkpointer
    with PostgresSaver.from_conn_string(POSTGRES_URI) as checkpointer:
        # 第一次装载数据库
        checkpointer.setup()
        # 这里可以赋值
        graph.checkpointer = checkpointer
        # 简单的流程，先生成再执行
        if not codeRequest.resume_code:
            response = graph.invoke(input=input_message, config=config)
        else:
            human_response = codeRequest.resume_code
            human_command = Command(resume={"code": human_response})  # 恢复断点
            response = graph.invoke(human_command, config=config)
    return response
