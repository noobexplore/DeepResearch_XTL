#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Author: GODTAO
@Contact: taoling.xu@transwarp.io
@File: api_conf.py
@Time: 2025/7/28 18:49
"""
# -*- coding: utf-8 -*-

import os
import fastapi
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from packaging.version import Version
from pydantic import BaseModel, Field

from src.planAgent.utils.tools import ProjectRootPath
from enum import Enum
from typing import Dict, Sequence


class _Cfg:
    title = "coder master"
    description = "coder master"


################################################################
# Misc
################################################################
# swagger local resource {
path_static = os.path.join(
    ProjectRootPath,
    "resource",
    (
        "static/swagger-ui-5"
        if Version(fastapi.__version__) > Version("0.98.0")
        else "static/swagger-ui"
    ),
)


def swagger_monkey_patch(*args, **kwargs):
    """离线`/docs`"""
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_favicon_url="/static/favicon.png",
        swagger_css_url="/static/swagger-ui.css",
        swagger_js_url="/static/swagger-ui-bundle.js",
    )


class ApiDetail(BaseModel):
    summary: str | None = Field(None)
    description: str | None = Field(None)
    tags: Sequence | None = Field(None)


def redoc_monkey_patch(*args, **kwargs):
    """离线`/redoc`"""
    return get_redoc_html(
        *args,
        **kwargs,
        redoc_js_url="/static/redoc.standalone.js",
    )


# 业务 {
class APIPathLlmEnum(str, Enum):
    """code api"""

    CODER_MASTER = "/gen"


ApiDetailsLlm: Dict[str, ApiDetail] = {
    APIPathLlmEnum.CODER_MASTER: ApiDetail(summary="生成执行代码"),
}


class APIRouterEnum(str, Enum):
    """路由地址"""

    CODE = "/code"


TagsAPIRoute: Dict[str, str] = {
    APIRouterEnum.CODE: "coder master执行接口",
}
