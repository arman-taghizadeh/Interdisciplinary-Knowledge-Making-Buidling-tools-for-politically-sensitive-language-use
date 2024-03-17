# Interdisciplinary-Knowledge-Making-Buidling-tools-for-politically-sensitive-language-use
Blockseminar: Interdisciplinary Knowledge-Making: Buidling tools for politically sensitive language use (WiSe 2023/24)
Project: Sensitive Language Identifier 

** check the requierment.txt for installing all necessary python libraries
** the Open AI api key is removed from our implementation, you need to replace your key in every api_key

This Flask application is a web-based tool for analyzing and processing PDF and image files using OpenAI's GPT model:

1. Importing Libraries: The necessary libraries such as Flask, PyPDF2, base64, requests, and OpenAI are imported.

2. Setting up Flask App: An instance of the Flask app is created, and the upload folder for storing files is defined.
3. Routes:
   - `/`: Renders the home page template.
   - `/upload`: Handles file uploads and processing. It extracts text from uploaded PDF files, analyzes images using GPT model, and renders the upload template with the processed data.
      - `/check`: Handles text evaluation requests for sensitive content.

4. Functions:
   - `predict_step1`, `predict_step2`: These functions use GPT model to extract text from images and analyze image contents, respectively.
   - `sensitive_check`: Evaluates text for sensitive content using the GPT model.
   - `encode_image`: Encodes images as base64 strings for use in API requests.
   - `save_file`: Saves uploaded files to the ‘uploads’ folder.
   - `get_temporary_url`: Generates temporary URLs for uploaded images.

5. Main Functionality:
   - The `/upload` route is the main functionality of the app. It processes uploaded files, extracts text from PDFs, analyzes images, and renders the results in the upload template.

Requirements to set up this project:
- Python installed on your system.
- Required libraries installed (Flask, PyPDF2, OpenAI, etc.). You can install them using pip.
- OpenAI API key for GPT model access (replace your key at every api_key)
- HTML templates (home.html, upload.html) for rendering web pages.
- Run the Flask app (webapp.py).
