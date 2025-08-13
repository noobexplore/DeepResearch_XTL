#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Author: GODTAO
@Contact: taoling.xu@transwarp.io
@File: state.py
@Time: 2025/6/25 19:09
"""
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState


class codeContent(BaseModel):
    """保存代码内容"""
    code_str: str = Field(description="保存生成的代码内容")


class CodeState(MessagesState):
    """整个状态保存"""
    command_txt: str  # 保存的代码
    code_res: str  # 代码执行的结果
    sample_data_input: str  # 示例的输入
    sample_data_output: str  # 示例的输出
    data_logical: str  # 转化逻辑描述
