FROM python:3.11-slim

WORKDIR /app/mcp-server

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py tools.py ./

EXPOSE 8000

CMD ["python", "server.py"]
