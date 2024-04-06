import logging
import requests

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image
import mysql.connector


from transformers import pipeline
from io import BytesIO

logging.basicConfig(level = logging.INFO)


def load_model(MODEL_NAME):
    global model
    try:
        logging.info(f'Loading {MODEL_NAME} pipeline')
        model = pipeline("image-to-text", model=MODEL_NAME)
        logging.info(f'Pipeline {MODEL_NAME} loaded successfully!')
    except Exception as e:
        return

def img2db(image, caption):
    logging.info(f'Connecting to the database')
    try:
        db_connection = mysql.connector.connect(
                        host="db",
                        port = 3306,
                        user="my_user",
                        password="my_password",
                        database="captioning"
                        )
        logging.info(f'Connected successfully to the database!')
    except Exception as e:
        logging.error(f'An error occured while connecting to the database\n{str(e)}')
        return
    db_cursor = db_connection.cursor()
    
    insert_query = "INSERT INTO Images (caption, image_file) VALUES (%s, %s)"
    insert_data = (caption, image)

    db_cursor.execute(insert_query, insert_data)
    db_connection.commit()

    db_cursor.close()
    db_connection.close()


class URLRequestModel(BaseModel):
    url: str
    language: str = 'English'
    prompt: str = 'Describe'
    push_db: bool = False


class PredictionResponseModel(BaseModel):
    prediction: str
    prompt: str
    model_name: str
    language: str


MODEL_NAME = 'Salesforce/blip-image-captioning-base' # TODO: add option to select pretrained model


try: 
    model = load_model(MODEL_NAME)
    logging.info(f'Model {MODEL_NAME} loaded succesfully!')
except Exception as e:
    logging.error(f'Model loading failed! Error: {str(e)}\nKilling app.')
    # Killing app
    import os
    import signal
    pid = os.getpid()
    os.kill(pid, signal.SIGKILL)



app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/model_name/')
async def getmodelname():
    logging.info(f'Received GET request on /model_name/')
    return {'model_name': MODEL_NAME}



@app.post('/change_model/')
def change_model(name:str):
    logging.info(f'Received POST request on /change_model/')
    try:
        global MODEL_NAME
        load_model(name)
        MODEL_NAME = name
        return {'result': 'success'}
    except Exception as e:
        logging.error(f'Failed to change model {str(e)}')

        return {'result': 'failed'}


@app.post("/predict_image_file/")
async def predict(language: str = 'English', prompt: str = 'what is it', file: UploadFile = File(...), push_db: bool = False):
    logging.info(f'Received POST request on /predict_image_file/')
    if not file.content_type.startswith('image/'):
        return JSONResponse(status_code=415, content={"message": "Only image files are allowed"})
    
    file_data = file.file.read()
    
    image = Image.open(BytesIO(file_data)).convert('RGB')

    output_text = model(image)[0]['generated_text']

    if push_db:
       img2db(file_data, caption=output_text)

    return PredictionResponseModel(prediction = output_text, 
                                   prompt = prompt,
                                   model_name=MODEL_NAME,
                                   language = language)

@app.post("/predict_image_url/")
async def predict_url(request_data: URLRequestModel):
    logging.info(f'Received POST request on /predict_image_url/')
    response = requests.get(request_data.url)
    response.raise_for_status()  # Raise an exception for bad status codes

    # Open the image using PIL's Image class
    image = Image.open(BytesIO(response.content)).convert("RGB")
    output_text = model(image)[0]['generated_text']

    if request_data.push_db:
        img2db(response.content, caption = output_text)

    return PredictionResponseModel(prediction = output_text, 
                                prompt = request_data.prompt,
                                model_name=MODEL_NAME,
                                language = request_data.language)


