FROM python:3.13-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有代码和文件
COPY . .

# 暴露Streamlit默认端口
EXPOSE 8501

# 默认命令
CMD ["streamlit", "run", "streamlit_app.py"]