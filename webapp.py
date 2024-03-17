

# importing necessary libraries:
from flask import  url_for, send_from_directory,Flask, render_template, request
import os
from PyPDF2 import PdfReader
import base64
import requests
from openai import OpenAI


#openai.api_key = ''

app = Flask(__name__, static_url_path='/static', static_folder='uploads')

# Define the upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/upload', methods=['POST'])
def upload():
    global text1, text2, text3, image_url2, image_url3,image_url2_1,image_url3_1,file1

    text1 = None
    text2 = None
    image_url2 = None
    text3 = None
    image_url3 = None
    sens2 = None
    sens3 = None
    if 'file1' in request.files:
        file1 = request.files['file1']
        if file1:
            reader = PdfReader(file1)
            text1 = []
            pages = reader.pages
            for p in pages:
                t = p.extract_text()
                text1.append(t)

    if 'file2' in request.files:
        file2 = request.files['file2']
        if file2:
            file2_path = save_file(file2)
            image_url2 = '/uploads/' + os.path.basename(file2_path)
            image_url2 = url_for('uploaded_file', filename=os.path.basename(file2_path).lstrip('/'))
            if image_url2.startswith('/'):
                image_url2_1 = image_url2[1:]
            text2 = predict_step1(image_url2_1)
            print('extracted text: ',text2)
            sens2 = sensitive_check(text2)
            print('evaluation: ',sens2)
    if 'file3' in request.files:
        file3 = request.files['file3']
        if file3:
            file3_path = save_file(file3)

            # Construct the URL for the uploaded file, removing leading '/'
            image_url3 = url_for('uploaded_file', filename=os.path.basename(file3_path).lstrip('/'))
            if image_url3.startswith('/'):
                image_url3_1 = image_url3[1:]

            text3 = predict_step2(image_url3_1)
            print('description: ',text3)
            sens3 = sensitive_check(text3)
            print('evaluation: ',sens3)

    if request.form.get('file_type') == 'pdf':
        show_text_container = True
    else:
        show_text_container = False



    return render_template('upload.html',text1 = text1 if text1 else None, text2 = text2 if text2 else None, text3=text3 if text3 else None, image_url2=image_url2, image_url3=image_url3,sens3=sens3 if sens3 else None,sens2=sens2 if sens2 else None,show_text_container=show_text_container)


##############################################

def predict_step2(image_path):

    # Get the absolute path of the image
    absolute_image_path = os.path.join(app.root_path, image_path.lstrip('/'))

    # Check if the file exists
    if not os.path.exists(absolute_image_path):
        print(f"Error: File not found at path: {absolute_image_path}")
        return None
    # OpenAI API Key
    api_key = ''

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    preds = response.json()

    return preds['choices'][0]['message']['content']

##############################################

# evaluating image by using GPT 3.5 language model
def sensitive_check(imgg):

    client = OpenAI(api_key = '')
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",

        messages=[
            {
                "role": "user",
                "content": f"evaluate this image for possible sexual content, sexism, racism, and related topics: {imgg}"
            }
        ]
    )
    preds = response.choices[0].message.content


    return preds

######################################################

# extracting text included in image using GPT 3.5 language model
def predict_step1(image_path):

    # Get the absolute path of the image
    absolute_image_path = os.path.join(app.root_path, image_path.lstrip('/'))

    # Check if the file exists
    if not os.path.exists(absolute_image_path):
        print(f"Error: File not found at path: {absolute_image_path}")
        return None

    # OpenAI API Key
    api_key = ''


    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "extract the text in this image"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())
    preds = response.json()

    return preds['choices'][0]['message']['content']

###############################################

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

################################################
def save_file(file):
    # Save the uploaded file to the uploads folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    return file_path

################################################
def get_temporary_url(file_path):
    # Generate a temporary URL for the uploaded image
    return '/' + file_path

#################################################
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Serve the uploaded files from the uploads folder
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
##################################################

@app.route('/check', methods=['POST'])
def check():

    textToCheck = request.form.get('text_to_check')
    client = OpenAI(api_key = '')

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",

        messages=[
            {
                "role": "user",
                "content": f"evaluate this text for possible sexual content, sexism, racism, and related topics: {textToCheck}"
            }
        ]
    )
    preds = response.choices[0].message.content

    return preds

#####################################################




if __name__ == '__main__':
    app.run(debug=True)




