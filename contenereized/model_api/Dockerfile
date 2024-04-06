FROM python:3.10-slim

ENV API_URL=http://model_api:5000

ENV DB_HOST=db
ENV DB_USER=my_user
ENV DB_PASSWORD=my_password
ENV DB_DATABASE=captioning



WORKDIR /api
COPY . /api

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]