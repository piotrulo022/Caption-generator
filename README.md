# Caption generator application built with microservices
This is a repository of project for web application that generates description for images. Descriptions are made using ready-made models from the transformers library.


https://github.com/piotrulo022/Caption-generator/assets/76213314/6f64147d-5da3-4782-87df-1db7e02c5b12

The project was developed in Python and consists of three microservices - a UI application written using Streamlit, a backend microservice providing prediction tools, and a database storing user-saved predictions. The application is containerized using Docker.

![captioning-architecture](https://github.com/piotrulo022/Caption-generator/assets/76213314/03200b09-2731-4a65-bc9f-302aaae82f6c)
You can find documentation of every microservice in its 
# How to run
All you need to run the application is docker. If you have it installed just clone this repository and build docker containers.

```bash
git clone https://github.com/piotrulo022/Caption-generator.git
cd Caption-generator
docker compose build && docker compose up
```

> [!WARNING]
> This application fetches large *image-to-seq* models, therefore it requires a stable and fairly fast internet connection to operate smoothly. Thus the initial run might take some time as the default model is being downloaded.
