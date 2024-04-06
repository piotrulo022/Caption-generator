import mysql.connector
import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO

def get_data():
    db_connection = mysql.connector.connect(
                host="db",
                port = 3306,
                user="my_user",
                password="my_password",
                database="captioning"
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
    st.title('# Gallery!')
    data = get_data()

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




    for ind, row in df.iterrows():
        image = decode_image(row['image_file'])
        image.resize((128, 64))
        caption = row['caption']
        created_time = row['created_time']
        
        image_col, mid, caption_col = st.columns([3, 1, 2])
        
        image_col.image(image, caption = 'Created at: ' + str(created_time))

        caption_col.markdown(f'<p class="caption-font"> {caption} </p>', unsafe_allow_html=True)
