from fastapi.testclient import TestClient
import sys

sys.path.append("..")
from api import app

client = TestClient(app)

# Get methods
def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json()['message'] == 'Hello World!'

def test_get_model_name():
    response = client.get('/model_name/')
    assert response.status_code == 200
    assert response.json()['model_name'] is not None


def test_predict_url():
    response = client.post('/predict_image_url/',
                            json = {'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/1200px-Google_2015_logo.svg.png',
                                    'prompt': 'ss',
                                    'push_db': False})
    
    assert response.status_code == 200

def test_predict_file():
    from PIL import Image
    from io import BytesIO

    with open("elephantoo.png", "rb") as file:
        bytes_data = BytesIO(file.read())

    filename = getattr(bytes_data, 'name', None)
    
    image = Image.open(bytes_data)
    filetype = image.format


    files = {'file': (filename, bytes_data, filetype)}

    response = client.post('/predict_image_file/', files = files,
                                                json = {'prompt': 'ss',
                                                'push_db': False})
    

    assert response.status_code == 200
