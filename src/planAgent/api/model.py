#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Author: GODTAO
@Contact: taoling.xu@transwarp.io
@File: model.py
@Time: 2025/7/28 18:49
"""
from enum import IntEnum
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union


class WdApiBaseResponse(BaseModel):
    """通用应答报文"""

    status: int = Field(description="结果状态")
    message: Optional[str] = Field(None, description="结果详情")


class WdApiStatus(IntEnum):
    """接口状态码"""

    SUCCESS = 0
    INVALID_REQ = 1
    INTERNAL_ERROR = 2
    LLM_ERROR = 3
    NOT_FOUND = 404
    UNKNOWN = 999


class CoderMetadata(BaseModel):
    """代码生成元数据，包含线程ID，用户ID，项目名之类的"""
    thread_id: str = Field(default="xtl01", description="会话线程ID")
    user_id: Optional[str] = Field(default="xtl007", description="会话用户ID")
    project_name: Optional[str] = Field(default="xtl", description="项目名称")


class CoderRequest(BaseModel):
    """代码生成接口"""
    input_data: Union[List[Dict[Any, Any]] | Dict[Any, Any] | str] = Field(..., description="用户数据输入")
    sample_data_input: Union[List[Dict[Any, Any]] | Dict[Any, Any] | str] = Field(..., description="示例数据输入")
    sample_data_output: Union[List[Dict[Any, Any]] | Dict[Any, Any] | str] = Field(..., description="示例数据输出")
    data_logical: str = Field(..., description="代码生成的逻辑描述")
    resume_code: str = Field(default="", description="审查过后的生成代码")
    agent_meta: Optional[CoderMetadata] = Field(description="相关的meta信息")
