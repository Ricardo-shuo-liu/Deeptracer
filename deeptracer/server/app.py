from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from deeptracer import DEEPTRACER_DEV_ROOT
import os
from typing import Any

def start(astAnalyer_html,speedAnalyer_html,workflowJson,originCode):
    app = FastAPI(
        title="deeptracer",
        description="link body",
    )
    # 创建节点
    static_path = os.path.join(DEEPTRACER_DEV_ROOT,"deeptracer/static")
    templates_path = os.path.join(DEEPTRACER_DEV_ROOT,"deeptracer/templates")
    # 获得路径
    app.mount("/static",StaticFiles(directory=static_path),name="static")
    templates = Jinja2Templates(directory=templates_path)
    # 读取模板和挂载文件
    @app.get("/",response_class=HTMLResponse, summary="前端页面入口")
    async def index(request:Request):
        try:
            print(f"Templates directory: {templates_path}")
            print(f"Template file exists: {os.path.exists(os.path.join(templates_path, 'index.html'))}")
            
            # 从参数提取数据
            py_file_code = originCode or '# 测试代码\ndef hello():\n    print("Hello, World!")\n\nhello()'
            if workflowJson:
                workflow_data = workflowJson
            else:
                workflow_data = {
                    'py_file_code': py_file_code,
                    'original_code': 'def hello():\n    print("Hello")\n\nhello()',
                    'modified_code': 'def hello():\n    print("Hello, World!")\n\nhello()',
                    'modify_reason': '添加了", World!"字符串，使输出更完整'
                }
            ast_html = astAnalyer_html or '<div style="padding: 20px; text-align: center;">AST可视化内容</div>'
            pyinstrument_html = speedAnalyer_html or '<div style="padding: 20px; text-align: center;">Pyinstrument性能分析内容</div>'
            
            print(f"Data prepared: py_file_code={py_file_code[:50]}..., workflow_data={workflow_data.keys()}")
            
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "workflow_data": workflow_data,
                    "py_file_code": py_file_code,
                    "ast_html": ast_html,
                    "pyinstrument_html": pyinstrument_html
                }
            )
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return HTMLResponse(content="<h1>404 - 文件不存在</h1>", status_code=404)
    @app.get("/{full_path:path}", response_class=HTMLResponse)
    async def catch_all(request: Request, full_path: Any = None):
        try:
            # 从参数提取数据
            py_file_code = originCode or '# 测试代码\ndef hello():\n    print("Hello, World!")\n\nhello()'
            if workflowJson:
                workflow_data = workflowJson
            else:
                workflow_data = {
                    'py_file_code': py_file_code,
                    'original_code': 'def hello():\n    print("Hello")\n\nhello()',
                    'modified_code': 'def hello():\n    print("Hello, World!")\n\nhello()',
                    'modify_reason': '添加了", World!"字符串，使输出更完整'
                }
            ast_html = astAnalyer_html or '<div style="padding: 20px; text-align: center;">AST可视化内容</div>'
            pyinstrument_html = speedAnalyer_html or '<div style="padding: 20px; text-align: center;">Pyinstrument性能分析内容</div>'
            
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "workflow_data": workflow_data,
                    "py_file_code": py_file_code,
                    "ast_html": ast_html,
                    "pyinstrument_html": pyinstrument_html
                }
            )
        except Exception as e:
            print(f"Error: {e}")
            return HTMLResponse(content="<h1>404 - 文件不存在</h1>", status_code=404)
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
    )
if __name__ == "__main__":
    start(None,None,{},None)