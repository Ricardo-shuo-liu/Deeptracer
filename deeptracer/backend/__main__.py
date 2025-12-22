from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import datetime
from io import BytesIO
import httpx  

app = FastAPI(
    title="前端部署+第三方工具JSON数据接口",
    description="部署前端页面 + 对接第三方工具生成JSON数据供前端使用",
    version="1.0"
)

# 项目路径配置
BASE_DIR = os.path.dirname(__file__)#当前文件目录
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")  # 前端文件目录

#  解决前端跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost：8571"], # 允许的前端地址
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# 前端页面部署（用户访问网址打开前端） 

# 挂载前端的CSS/JS/图片等静态文件
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
# 指定HTML模板目录，用于渲染前端入口页面
templates = Jinja2Templates(directory=FRONTEND_DIR)

# 根路径：返回前端入口页面(FROMTEND_DIR/index.html)
@app.get("/", response_class=HTMLResponse, summary="前端页面入口")
async def serve_frontend(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"前端页面加载失败：{str(e)}")

# 适配前端SPA路由（捕获所有未匹配路径，返回index.html）
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(request: Request, full_path: str):
    return templates.TemplateResponse("index.html", {"request": request})

# 对接第三方工具生成JSON数据 （先用HTTP请求方式）
async def get_third_party_data() -> dict:
    """
    对接第三方工具/接口(HTTP请求)，获取实时数据,后期根据工具再修改
    :return: 第三发方原始数据（字典格式）
    先按JSON格式处理，便于前端的渲染，后期根据实际情况调整
    """
    # 第三方工具
    third_party_url = "第三方工具接口地址"
    # 第三方工具请求参数（后期调整）        
    third_party_params = {
        "token": "your_tool_token",
        "type": "realtime_data"
    }

    try:
        # 异步调用第三方工具接口
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                url=third_party_url,
                params=third_party_params
                #根据前端提交的issue，暂为get请求，后期可改为post请求
            )
        response.raise_for_status()  # 校验响应状态
        
        # 获取第三方原始数据 （暂时返回JSON格式）
        raw_data = response.json() #若为其他格式，可更改
        return raw_data

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"第三方工具接口返回错误：{str(e)}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"第三方工具接口调用失败：{str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"第三方数据解析失败：{str(e)}")

def format_to_standard_json(raw_data: dict) -> dict:
    """
    将第三方原始数据转换为标准JSON格式，完成对数据的清洗和封装
    :param raw_data: 第三方原始数据
    :return: 标准化JSON数据
    看后续情况，如果工具返回的是XML，可用xmltodict来解析
    """
    # 示例：根据前端需求封装数据结构【AI生成，后期可按需修改数据封装格式】
    standard_data = {
        "meta": {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "data_source": "第三方数据工具V2.0",
            "version": "1.0"
            #封装其他元信息
        },
        "business_data": {
            # 提取第三方核心数据
            "sensor_list": raw_data.get("sensor_list", []),
            "total_count": raw_data.get("total", 0),
            "status": raw_data.get("status", "unknown"),
            "extend_info": raw_data.get("extend", {})
        },
        "code": 200,
        "msg": "数据获取成功"
    }
    return standard_data

# 接口1：返回JSON内容（前端解析使用）
@app.get("/api/realtime-json", summary="获取JSON数据供前端解析")
async def get_realtime_json_content():
    """前端无需下载文件，能直接使用解析JSON内容"""
    # 1. 异步调用第三方工具获取原始数据
    raw_data = await get_third_party_data()
    # 2. 转换为标准JSON格式
    standard_json = format_to_standard_json(raw_data)
    # 3. 返回JSON响应（FastAPI自动序列化）
    return JSONResponse(content=standard_json, charset="utf-8")

#  接口2：返回JSON下载
@app.get("/download/realtime-json", summary="下载JSON文件，前端保存")
async def download_realtime_json_file():
    """前端下载JSON文件，无本地文件落地，内存中生成"""
    # 1. 获取第三方原始数据
    raw_data = await get_third_party_data()
    # 2. 转换为标准JSON格式
    standard_json = format_to_standard_json(raw_data)
    # 3. 序列化为JSON字符串
    json_str = json.dumps(standard_json, ensure_ascii=False, indent=2)
    json_bytes = json_str.encode("utf-8")
    # 4. 生成内存字节流
    json_stream = BytesIO(json_bytes)
    json_stream.seek(0)  
     # 5. 生成带时间戳的文件名
    filename = f"realtime_data_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    
    # 6. 触发下载
    return StreamingResponse(
        content=json_stream,
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Length": str(len(json_bytes))  # 告知前端文件大小
        }
    )

if __name__ == "__main__":
    import uvicorn
    # 启动服务（host=0.0.0.0允许局域网/公网访问）
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True, 
        workers=1     
    )