from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.endpoints import auth, comics, chapters, reader
from app.db.base import Base, engine
import socket

app = FastAPI(title=settings.PROJECT_NAME)

# 首先挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(comics.router, prefix="/api/comics", tags=["comics"])
app.include_router(chapters.router, prefix="/api/chapters", tags=["chapters"])
app.include_router(reader.router, prefix="/api/reader", tags=["reader"])

# 创建数据库表
Base.metadata.create_all(bind=engine)

def get_local_ip():
    try:
        # 获取本机主机名
        hostname = socket.gethostname()
        # 获取本机IP地址
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except Exception as e:
        print(f"获取本地IP失败: {e}")
        return "0.0.0.0"

if __name__ == "__main__":
    import uvicorn
    host = "0.0.0.0"  # 监听所有网络接口
    port = 8812
    local_ip = get_local_ip()
    print(f"\n服务器已启动:")
    print(f"本机访问: http://localhost:{port}")
    print(f"局域网访问: http://{local_ip}:{port}")
    uvicorn.run(app, host=host, port=port) 