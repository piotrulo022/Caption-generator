# measuring prediction time
from time import time

# web modules
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

# image processing
from PIL import Image
from io import BytesIO


# global variables, data models and important functions
from api_utils import *

################### Initialization step - loading default model ################### 

def load_model(MODEL_NAME: str) -> None:
    """
    This function changes globally used model for generating caption.

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

try: 
    load_model(MODEL_NAME)
except Exception as e:
    logging.error(f'Model loading failed! Error: {str(e)}\nKilling app.')
    import os
    import signal
    pid = os.getpid()
    os.kill(pid, signal.SIGKILL)


################### FastAPI and its endpoints ################### 

app = FastAPI()


# GET METHODS
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




# POST METHODS

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

    return ChangeModelResponseModel(result=status)


@app.post("/predict_image_file/", tags = ['Prediction'])
async def predict(file: UploadFile = File(...), push_db: bool = False):
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
                                   used_model_name=MODEL_NAME,
                                   processing_time=str(processing_time))



@app.post("/predict_image_url/", tags = ['Prediction'])
async def predict_url(request_data: PredictURLRequestModel):
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
                                    used_model_name = MODEL_NAME,
                                    processing_time = str(processing_time))

# DELETE METHODS

@app.delete('/purge_database/')
def delete_database():
    """
    Delete everything from table that stores images.
    """
    logging.info(f'Received DELETE request on /purge_database/')


    result = delete_table()
    return DeleteDataResponseModel(result = result)


@app.delete('/delete_row/')
async def delete_single_row(request_data: DeleteRowRequestModel):
    """
    Delete single row from table that stores images. Row is being found by given `created_time` and `caption` params and deleted.
    """
    logging.info(f'Received DELETE request on /delete_row/')

    result = delete_data(request_data.caption, request_data.created_time)

    return DeleteDataResponseModel(result = result)
