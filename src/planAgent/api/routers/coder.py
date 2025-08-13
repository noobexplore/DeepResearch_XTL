#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Author: GODTAO
@Contact: taoling.xu@transwarp.io
@File: coder.py
@Time: 2025/7/28 18:57
"""
from fastapi import APIRouter
from ..model import CoderRequest
from src.planAgent.graph import coder_master_sync
from ..api_conf import ApiDetailsLlm, APIPathLlmEnum, APIRouterEnum, TagsAPIRoute


router = APIRouter(
    prefix=APIRouterEnum.CODE,
    tags=[TagsAPIRoute[APIRouterEnum.CODE]],
)


# text2sql服务
@router.post(
    APIPathLlmEnum.CODER_MASTER,
    **ApiDetailsLlm[APIPathLlmEnum.CODER_MASTER].model_dump(),
)
def code_master_api(code_req: CoderRequest):
    """
    代码大师请求API
    Args:
        code_req:代码生成请求内容

    Returns:

    """
    response_code = coder_master_sync(code_req)
    if "__interrupt__" in response_code:
        response = response_code['__interrupt__'][0].value["command_txt"]
        response = {"review": False, "code_view": response}
    else:
        response = {"review": True, "code_execute": response_code["code_res"]}
    return response
