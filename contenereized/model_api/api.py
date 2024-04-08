# utils
import logging
import os
from time import time


# web modules
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# database management
import mysql.connector

# models for caption generation
from transformers import pipeline

# data management
from PIL import Image
from io import BytesIO

logging.basicConfig(level = logging.INFO) # logging module settings


################### GlobaL variables ################### 
                                                       
MODEL_NAME = 'tarekziade/deit-tiny-distilgpt2' # default model

# Database authentication
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DATABASE = os.environ.get('DB_DATABASE')

################### Request/Response models ################### 
class URLRequestModel(BaseModel):
    """
    Expected data model for requests for prediction image from URL.
    """
    url: str
    prompt: str = 'Describe'
    push_db: bool = False


class PredictionResponseModel(BaseModel):
    """
    Response data model.
    """
    prediction: str
    prompt: str
    processing_time: str
    model_name: str


class ChangeModelResponseModel(BaseModel):
    result: str

################### Util functions ################### 

def load_model(MODEL_NAME: str) -> None:
    """
    This funcion changes globally used model for generating caption.

    # Arguments:

    - `MODEL_NAME`:str - model name desired to be used as caption generator. 
    
    """
    global model
    try:
        logging.info(f'Loading {MODEL_NAME} pipeline')
        model = pipeline("image-to-text", model=MODEL_NAME)
        logging.info(f'Pipeline {MODEL_NAME} loaded successfully!')
    except Exception as e:
        logging.error(f'Error while loading {MODEL_NAME}! {str(e)}')
        return



def img2db(image, caption)-> None:
    """
    Push instance (image, caption) to the database.
    
    """
    try:
        logging.info('Connecting to the database')
        with mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_DATABASE
            ) as db_connection:
            logging.info('Connected successfully to the database!')
            
            db_cursor = db_connection.cursor()
            
            insert_query = "INSERT INTO Images (caption, model_used, image_file) VALUES (%s, %s, %s)"
            insert_data = (caption, MODEL_NAME, image)

            db_cursor.execute(insert_query, insert_data)
            db_connection.commit()
            
            logging.info('Image inserted successfully into the database')

    except mysql.connector.Error as e:
        logging.error(f'An error occurred while connecting to or interacting with the database: {e}')
        raise  # Re-raise the exception to let the caller handle it

    except Exception as e:
        logging.error(f'An unexpected error occurred: {e}')
        raise  # Re-raise the exception




################### Initialization step - loading default model ################### 
try: 
    load_model(MODEL_NAME)
except Exception as e:
    logging.error(f'Model loading failed! Error: {str(e)}\nKilling app.')
    # Killing app
    import os
    import signal
    pid = os.getpid()
    os.kill(pid, signal.SIGKILL)




################### FastAPI and its endpoints ################### 

app = FastAPI()


@app.get("/", include_in_schema = False)
async def root():
    """
    Home endpoint.
    """
    return {"message": "Hello World!"}

@app.get('/model_name/')
async def getmodelname():
    logging.info(f'Received GET request on /model_name/')
    return {'model_name': MODEL_NAME}



@app.post('/change_model/', tags=['Model config'])
def change_model(name:str):
    """
    Post endpoint used to caption generator
    """

    logging.info(f'Received POST request on /change_model/')
    
    try:
        global MODEL_NAME
        load_model(name)
        MODEL_NAME = name
        status = 'success'
    except Exception as e:
        status = 'failed'
    # return {'result': 'failed'}
    return ChangeModelResponseModel(result=status)



@app.post("/predict_image_file/", tags = ['Prediction'])
async def predict(prompt: str = 'what is it', file: UploadFile = File(...), push_db: bool = False):
    """
    Generate caption for a uploaded image file.
    """

    logging.info(f'Received POST request on /predict_image_file/')

    if not file.content_type.startswith('image/'): # Validate data type
        return JSONResponse(status_code=415, content={"message": "Only image files are allowed"})
    
    # process data to 
    file_data = file.file.read()
    logging.info(f'Type of filedata: {type(file_data)}')
    
    image = Image.open(BytesIO(file_data)).convert('RGB')

    # measure processing itme
    start_time = time()
    
    output_text = model(image)[0]['generated_text']

    if push_db:
       img2db(file_data, caption=output_text)
    
    end_time = time()


    processing_time = end_time - start_time

    return PredictionResponseModel(prediction = output_text, 
                                   prompt = prompt,
                                   model_name=MODEL_NAME,
                                   processing_time=str(processing_time))





@app.post("/predict_image_url/", tags = ['Prediction'])
async def predict_url(request_data: URLRequestModel):
    """
    Generate caption for a given URL containing image.
    """

    logging.info(f'Received POST request on /predict_image_url/')
    response = requests.get(request_data.url)
    response.raise_for_status()  # Raise an exception for bad status codes


    image = Image.open(BytesIO(response.content)).convert("RGB")

    # Measure time
    start_time = time()
    
    output_text = model(image)[0]['generated_text']

    if request_data.push_db:
        img2db(response.content, caption = output_text)

    end_time = time()

    processing_time = end_time - start_time

    return PredictionResponseModel(prediction = output_text, 
                                prompt = request_data.prompt,
                                model_name = MODEL_NAME,
                                processing_time = str(processing_time))
