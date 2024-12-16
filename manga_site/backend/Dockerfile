# 使用官方Python基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app/backend

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 设置pip使用清华镜像源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 先复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制其他项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p uploads static data

# 暴露端口
EXPOSE 8812

# 添加健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8812/health || exit 1

CMD ["python", "main.py"] 