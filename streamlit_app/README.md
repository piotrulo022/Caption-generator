# UI microservice 

This folder contains the source code for a UI application built with the Streamlit framework. It serves as the primary interface through which users interact with the software. The UI is the front-facing component where users directly engage with various features and functionalities.

![image](https://github.com/piotrulo022/Caption-generator/assets/76213314/7b021615-5c46-4b2c-a03e-80f6bfa3c020)


Operations performed by the client within the UI interface trigger requests sent to the backend. Subsequently, the received responses are displayed back to the user. This seamless interaction between the frontend and backend ensures smooth functionality and an intuitive user experience.

# Folder structure description
- `Dockerfile` - file containing a set of instructions used to build a Docker image;
- `requirements.txt` - set of packages installed in docker container needed for application to work;
- `main.py` - main application script;
- `homepage.py`, `config.py`, `get_caption.py`, `database_preview.py` - each of these script refers to page in application;
- `util_funs.py` - utility functions that provide functionalities to application.
