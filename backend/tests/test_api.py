import sys
import sqlite3
from fastapi.testclient import TestClient

sys.path.append("..")
from api import app


client = TestClient(app)

# GET methods
def test_read_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json()['message'] == 'Hello World!'

def test_get_model_name():
    response = client.get('/model_name/')
    assert response.status_code == 200
    assert response.json()['model_name'] is not None

# POST methods

def test_predict_url():
    response = client.post('/predict_image_url/',
                            json = {'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Google_2015_logo.svg/1200px-Google_2015_logo.svg.png',
                            'push_db': False})
    
    assert response.status_code == 200

def test_predict_file():
    image = open("elephantoo.png", "rb")

    files = {'file': ('elephant', image, 'image/png')}
    response = client.post('/predict_image_file/', files = files, json = {'push_db': False})
    
    assert response.status_code == 200


# DELETE methods

def test_purge_database():

    def delete_table(): # create dummy database and delete images exactly like in API
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Images (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            caption TEXT,
                            model_used TEXT,
                            image_file BLOB NOT NULL,
                            created_time TEXT DEFAULT CURRENT_TIMESTAMP
                        )''')
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Images;")
            conn.commit()
            cursor.close()
            return 'success'
        except sqlite3.Error as err:
            return f"failed to delete row {str(err)}"
    

    result = delete_table()

    assert result == 'success'



def test_delete_row():

    def delete_row():
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Images (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            caption TEXT,
                            model_used TEXT,
                            image_file BLOB NOT NULL,
                            created_time TEXT DEFAULT CURRENT_TIMESTAMP
                        )''')
        try:
            # conditions for rows to be deleted
            created_time = "2024-04-14 19:08:54"
            caption = "foo"

            cursor = conn.cursor()
            cursor.execute("DELETE FROM Images WHERE caption = ? AND created_time = ?", (caption, created_time))
     
            conn.commit()
            cursor.close()
            return 'success'
        except sqlite3.Error as err:
            return f"failed to delete row {str(err)}"
    

    result = delete_row()

    assert result == 'success'


