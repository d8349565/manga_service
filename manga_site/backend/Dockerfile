# 使用官方Python基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app/backend

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


# 安装系统依赖
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# 设置pip使用清华镜像源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目文件
COPY . /app/backend/

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建必要的目录
RUN mkdir -p /app/backend/uploads /app/backend/static /app/backend/data

# 暴露端口
EXPOSE 8812

# 启动命令
CMD ["python", "main.py"] 