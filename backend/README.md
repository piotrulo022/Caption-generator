# Backend FastAPI server microservice

This folder includes files for backend container microservice that serve FastAPI endpoints. 

The microservice handles incoming HTTP requests from `streamlit_app` and communicates with the database. It handles the crucial task of returning model predictions. These predictions are often central to the functionality of the entire system, making this microservice a key component in the overall workflow.

FastAPI has been carefully designed according to the REST standard with attention to code readability. Functionality for monitoring and debugging using the `logging` module has also been implemented.

# Folder structure description

 - `/tests/` - includes API unit tests;
 - `Dockerfile` - file containing a set of instructions used to build a Docker image;
 - `api.py` - FastAPI script file;
 - `api_utils.py` - global variables, functions and data models for FastAPI.

# Endpoints description

This API consists of 5 endpoints where:
- ${\color{blue}@GET}$ `/model_name/` - returns name of currently selected model for description generation;
- ${\color{green}@POST}$ `/predict_image_file/` - returns prediction for given image file uploaded from local disk;
- ${\color{green}@POST}$ `/predict_image_url/` - returns prediction for given image given by its URL site location;
- ${\color{red}@DELETE}$ `/purge_database/` - remove all images along their captions stored in database;
- ${\color{red}@DELETE}$ `/delete_row/` - remove images where given *caption* and *created_time* params match.

![image](https://github.com/piotrulo022/Caption-generator/assets/76213314/cfb7f541-9146-4d22-a886-ba67afcd6720)

