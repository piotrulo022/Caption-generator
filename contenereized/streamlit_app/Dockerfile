FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5005

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=5005"]
