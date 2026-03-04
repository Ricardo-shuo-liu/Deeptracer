from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from deeptracer import DEEPTRACER_DEV_ROOT
import os

def start(astAnalyer,memoryAnalayer,speedAnalyer,workflow):
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
    @app.get("/")
    async def index(request:Request):
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
            }
        )

    uvicorn.run(
        "deeptracer.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
    )