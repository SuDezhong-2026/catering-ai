# 用 Python 3.13 精简版基础镜像（比完整版小很多）
FROM python:3.13-slim

# 工作目录，之后所有 COPY/命令都在这
WORKDIR /app

# 先只复制依赖清单并安装——这层会缓存，改代码不用重装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再复制整个项目（已用 .dockerignore 排除 .venv/.env/.git 等）
COPY . .

# 暴露端口（和下面 --port 对应）
EXPOSE 8000

# ★ 必须 --host 0.0.0.0，否则容器外访问不到
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
