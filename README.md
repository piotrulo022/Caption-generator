# Caption generator application built with microservices
This is a repository of project for web application that generates description for images. Descriptions are made using ready-made models from the transformers library.


https://github.com/piotrulo022/Caption-generator/assets/76213314/6f64147d-5da3-4782-87df-1db7e02c5b12

The project was developed in Python and consists of three microservices - a UI application written using Streamlit, a backend microservice providing prediction tools, and a database storing user-saved predictions. The application is containerized using Docker.

<p align="center">
  <img src="https://github.com/piotrulo022/Caption-generator/assets/76213314/03200b09-2731-4a65-bc9f-302aaae82f6c">
</p>

You can find documentation of every microservice in its directory.
# How to run
All you need to run the application is docker. If you have it installed just clone this repository and build docker containers.

```bash
git clone https://github.com/piotrulo022/Caption-generator.git
cd Caption-generator
docker compose build && docker compose up
```
> [!WARNING]
> This application fetches large *image-to-seq* models, therefore it requires a stable and fairly fast internet connection to operate smoothly. Thus the initial run might take some time as the default model is being downloaded.

# References
- <img src="https://github.com/piotrulo022/Caption-generator/assets/76213314/041bc9c8-bbaa-46fe-b36a-80c34be01694" width="35" height="23"/> [Streamlit - A faster way to build and share data apps](https://streamlit.io/)
- <img src="https://github.com/piotrulo022/Caption-generator/assets/76213314/ba8ce534-07dc-4ab9-9944-64e39e7d37c9" width="35" height="23"/> [Huggingface - The AI community building the future.](https://huggingface.co/)
- <img src="https://github.com/piotrulo022/Caption-generator/assets/76213314/78ea06b0-00cd-4081-bc09-d31f6860b992" width="35" height="23"/> [Docker - Accelerated Container Application Development](https://www.docker.com/)
- <img src="https://github.com/piotrulo022/Caption-generator/assets/76213314/7d6a0917-fd64-47e3-a8d2-80236766e1fb" width="35" height="23"/> [FastAPI framework](https://fastapi.tiangolo.com/)
- <img src="https://github.com/piotrulo022/Caption-generator/assets/76213314/2aeef1f8-144e-44c6-b98d-9307c9b3471e" width="35" height="23"/> [Knowledge](https://dwojcik92.github.io/) - visit author's github contents [here](https://github.com/dwojcik92/).
