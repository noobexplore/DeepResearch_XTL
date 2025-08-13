#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@Author: GODTAO
@Contact: taoling.xu@transwarp.io
@File: tools.py
@Time: 2025/6/25 19:08
"""
import os
import re
import sys
import json
import subprocess
from pathlib import Path
from langchain_experimental.utilities import PythonREPL

ProjectRootPath = Path(os.path.abspath(__file__)).parent.parent

python_repl = PythonREPL()


def install_package(pkg):
    """如果有相关依赖包用该工具进行安装依赖"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])


def safe_python_repl(code):
    # 使用三重引号包起来防止转义符号
    # safe_code = f"""{code}"""
    safe_code = code
    safe_code = python_repl.sanitize_input(safe_code)
    run_res = python_repl.run(safe_code)
    # 先判断是否缺少依赖
    if "ModuleNotFoundError" in run_res:
        match = re.search(r"No module named '([^']+)'", run_res)
        if match:
            module_name = match.group(1)
            install_package(module_name)
            run_res = python_repl.run(safe_code)
    # 再判断是否有些其他错误
    if "Error" not in run_res:
        run_res = eval(run_res)
    return run_res
