FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH="${PYTHONPATH}:/app"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /app
CMD ["uvicorn", "src.fastapi_app.fastapi_app:app", "--host", "0.0.0.0", "--port", "8001"]
