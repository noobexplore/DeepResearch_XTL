#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Author: GODTAO
@Contact: taoling.xu@transwarp.io
@File: configure.py
@Time: 2025/7/28 11:08
"""
import os
from pydantic import BaseModel, Field
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig


class Configuration(BaseModel):
    """The configuration for the agent."""

    coder_model: str = Field(default="Qwen/Qwen3-30B-A3B", description="代码生成大模型")
    temperature: str = Field(default=0.6, description="代码生成大模型")
    max_tokens: str = Field(default=20000, description="最大token长度")
    enable_thinking: str = Field(default=False, description="是否开启思考")

    @classmethod
    def from_runnable_config(
            cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )

        # Get raw values from environment or config
        raw_values: dict[str, Any] = {
            name: os.environ.get(name.upper(), configurable.get(name))
            for name in cls.model_fields.keys()
        }

        # Filter out None values
        values = {k: v for k, v in raw_values.items() if v is not None}

        return cls(**values)
