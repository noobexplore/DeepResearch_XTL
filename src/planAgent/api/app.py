#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Author: GODTAO
@Contact: taoling.xu@transwarp.io
@File: app.py
@Time: 2025/7/28 18:46
"""
# -*- coding: utf-8 -*-
import uuid
import uvicorn
from fastapi import FastAPI, applications, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from src.planAgent.api.api_conf import _Cfg, path_static, redoc_monkey_patch, swagger_monkey_patch
from src.planAgent.api.model import WdApiBaseResponse, WdApiStatus

from src.planAgent.api.routers import coder

app = FastAPI(
    title=_Cfg.title,
    description=_Cfg.description,
    # docs_url="/apidocs",
)

# 设置本地静态资源 {
app.mount("/static", StaticFiles(directory=path_static), name="static")

applications.get_swagger_ui_html = swagger_monkey_patch  # type: ignore
applications.get_redoc_html = redoc_monkey_patch  # type: ignore
# }

# 设置中间件 {
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://0.0.0.0:5000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=uuid.uuid4().hex, max_age=None)

# }

app.include_router(coder.router)


@app.exception_handler(Exception)
async def any_exception_handler(
        request: Request, exc: Exception
):  # pylint: disable=W0613
    """接口级异常捕捉

    最后一道异常处理
    """
    return JSONResponse(
        status_code=200,
        content=WdApiBaseResponse(
            status=exc.errno if hasattr(exc, "errno") else WdApiStatus.UNKNOWN,
            message=exc.strerror if hasattr(exc, "strerror") else str(exc),
        ).model_dump(),
    )

# if __name__ == '__main__':
#     uvicorn.run(app='app:app', host='0.0.0.0', port=52024)
