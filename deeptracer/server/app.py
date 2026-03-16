from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from deeptracer import DEEPTRACER_DEV_ROOT
import os
from typing import Any

def start(astAnalyer,speedAnalyer,workflow):
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
        # TODO:补充模板填充以及前端代码
        try:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                }
            )
        except Exception:
            HTMLResponse(content="<h1>404 - 文件不存在</h1>", status_code=404)
    @app.get("/{full_path:path}", response_class=HTMLResponse)
    async def catch_all(request: Request, full_path: Any = None):
        try:
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                }
            )
        except Exception:
            HTMLResponse(content="<h1>404 - 文件不存在</h1>", status_code=404)
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
    )