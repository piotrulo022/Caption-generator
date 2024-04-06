FROM python:3.10-slim

ENV API_URL=http://model_api:5000

ENV DB_HOST=db
ENV DB_USER=my_user
ENV DB_PASSWORD=my_password
ENV DB_DATABASE=captioning

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5005

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=5005"]
