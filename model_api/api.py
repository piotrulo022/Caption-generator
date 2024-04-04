import logging
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image

from io import BytesIO
logging.basicConfig(level = logging.INFO)


class URLRequestModel(BaseModel):
    url: str
    language: str = 'English'
    prompt: str = 'Describe'

    

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
async def predict(language: str = 'English', prompt: str = 'what is it', file: UploadFile = File(...)):
    logging.info(f'Received request on /predict_image/')
    # file = await input_data.file.read()
    # Check if the uploaded file is an image
    if not file.content_type.startswith('image/'):
        return JSONResponse(status_code=415, content={"message": "Only image files are allowed"})
    image = Image.open(BytesIO(await file.read())).convert('RGB')

    inputs = processor(image, prompt, return_tensors = 'pt')
    out = model.generate(**inputs)
    
    output_text = processor.decode(out[0], skip_special_tokens=True)

    # return {'prediction': output_text,
    #         'prompt': prompt,
    #         'language': language}
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

    return PredictionResponseModel(prediction = output_text, 
                                prompt = request_data.prompt,
                                language = request_data.language)


