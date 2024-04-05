import logging
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image
import mysql.connector


from io import BytesIO
logging.basicConfig(level = logging.INFO)

def img2db(image, caption):
    db_connection = mysql.connector.connect(
                    host="db",
                    port = 3306,
                    user="my_user",
                    password="my_password",
                    database="captioning"
                    )
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
    language: str


MODEL_NAME = 'Salesforce/blip-image-captioning-base' # TODO: add option to select pretrained model

logging.info(f'Loading {MODEL_NAME} model')
try:
    processor = BlipProcessor.from_pretrained(MODEL_NAME)
    model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)
    logging.info(f'Model {MODEL_NAME} loaded succesfully!')
except Exception as e:
    logging.error(f'Model loading failed! Error: {str(e)}\nKilling app.')
    # Killing app
    import os
    import signal
    pid = os.getpid()
    os.kill(pid, signal.SIGKILL)

app = FastAPI()


@app.post("/predict_image_file/")
async def predict(language: str = 'English', prompt: str = 'what is it', file: UploadFile = File(...), push_db: bool = False):
    logging.info(f'Received request on /predict_image/')
    # file = await input_data.file.read()
    # Check if the uploaded file is an image
    if not file.content_type.startswith('image/'):
        return JSONResponse(status_code=415, content={"message": "Only image files are allowed"})
    
    file_data = file.file.read()
    image = Image.open(BytesIO(file_data)).convert('RGB')

    inputs = processor(image, prompt, return_tensors = 'pt')
    out = model.generate(**inputs)
    output_text = processor.decode(out[0], skip_special_tokens=True)

    if push_db:
       img2db(file_data, caption=output_text)

    return PredictionResponseModel(prediction = output_text, 
                                   prompt = prompt,
                                   language = language)



@app.post("/predict_image_url/")
async def predict_url(request_data: URLRequestModel):
    response = requests.get(request_data.url)
    response.raise_for_status()  # Raise an exception for bad status codes

    # Open the image using PIL's Image class
    image = Image.open(BytesIO(response.content)).convert("RGB")

    out = processor(image, return_tensors = 'pt')
    out = model.generate(**out)

    output_text = processor.decode(out[0], skip_special_tokens = True)

    if request_data.push_db:
        img2db(response.content, caption = output_text)

    return PredictionResponseModel(prediction = output_text, 
                                prompt = request_data.prompt,
                                language = request_data.language)


