FROM python:3.11-slim

WORKDIR /app

# تثبيت المتطلبات النظامية الأساسية فقط
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# نسخ الملفات
COPY requirements.txt .
COPY *.py ./

# تثبيت متطلبات البايثون
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
