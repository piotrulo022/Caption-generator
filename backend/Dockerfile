FROM python:3.10-slim

ENV API_URL=http://backend:5000

# export environment variables to store information about database credientials
ENV DB_HOST=db
ENV DB_USER=my_user
ENV DB_PASSWORD=my_password
ENV DB_DATABASE=captioning

# set cwd and copy contents
WORKDIR /api
COPY . /api

# install dependencies and run script
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]
