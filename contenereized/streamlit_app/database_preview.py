import mysql.connector
import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO

import os

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DATABASE = os.environ.get('DB_DATABASE')

def get_data():
    db_connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_DATABASE
                )
    db_cursor = db_connection.cursor()
    
    query = "SELECT * FROM Images;"
    db_cursor.execute(query)

    data = db_cursor.fetchall()

    colnames = [column[0] for column in db_cursor.description]


    return {'data': data,
            'colnames': colnames}

def decode_image(file):
    image = Image.open(BytesIO(file)).convert('RGB')

    return image

def app():
    st.title('Gallery!')
    data = get_data()
    if not data:
        st.write('Nothing here yet. Generate some captions so they will apear here!')

    else:
        df = data['data']
        df = pd.DataFrame(df, columns=data['colnames'])

        st.markdown("""
                <style>
                .caption-font {
                    font-size:16px !important;
                    font-style: italic;
                }
                </style>
                """, unsafe_allow_html=True)
        

        c1, c2, c3 = st.columns([3, 1, 2], gap = 'medium')
        c1.markdown('## Image')
        c2.markdown('## Model used')
        c3.markdown('## Caption')
        
        for ind, row in df.iterrows():
            image = decode_image(row['image_file']) 
            image.resize((128, 64))

            caption = row['caption']
            
            created_time = row['created_time']
            
            model_used = row['model_used']


            image_col, model_col, caption_col = st.columns([3, 1, 2], gap = 'medium')
            
            image_col.image(image, caption = 'Created at: ' + str(created_time))
            
            model_col.markdown(f'*{model_used}*')

            caption_col.markdown(f'<p class="caption-font"> {caption} </p>', unsafe_allow_html=True)
