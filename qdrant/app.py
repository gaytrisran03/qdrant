from flask import Flask, render_template, request, jsonify, flash, redirect
from markupsafe import Markup 
from qdrant_client import models, QdrantClient
from qdrant_client.http.models import PointStruct
# from summarius import *
import re
import os, shutil
from PyPDF2 import PdfReader
import glob
from docx2pdf import convert
from sentence_transformers import SentenceTransformer
# import pinecone
from langchain.text_splitter import CharacterTextSplitter
import json
import time
from werkzeug.utils import secure_filename


model = SentenceTransformer('all-MiniLM-L6-v2')
client = QdrantClient(":memory:")
client.recreate_collection(
    collection_name="test_collection",
    vectors_config=models.VectorParams(
        size=model.get_sentence_embedding_dimension(), # Vector size is defined by used model
        distance=models.Distance.EUCLID
    )
)


app = Flask(__name__)


@app.route('/delete', methods=['POST'])
def deleteFiles():
    start = time.time()
    client.delete_collection(collection_name="test_collection")

    shutil.rmtree('./uploads/')
    os.makedirs('./uploads/')
    shutil.rmtree('./queryresume/')
    os.makedirs('./queryresume/')

    taken = time.time() - start
    print(f"Time taken to delete file : {taken:.2f} seconds.")
    # return 'Pinecone index cleared!'
    return render_template("result.html", result='Vector index, Upload Resume and Query Resume all  cleared!')

@app.route('/')
def index():
    return render_template('index1.html', files=os.listdir('./uploads'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if the directory exists, create it if necessary
        files= request.files.getlist("file")
        for file in files:
            file.save("./uploads/"+file.filename)

    return render_template('index1.html', Files = os.listdir('./uploads'))

@app.route('/vector', methods=['POST'])
def dbupload():

    start = time.time()

    docx_files=glob.glob('./uploads/*.docx')
    for docx in docx_files:
            convert(docx,'./uploads/')

    dir_name='./uploads'
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".docx"):
            os.remove(os.path.join(dir_name, item))
    

    folder = glob.glob('./uploads/*.pdf')
    #iterate over every pdf 
    id=0
    for pdf in folder :
    # read the pdf file
        pdf_reader=PdfReader(pdf)
        # print(pdf_reader)
        # iterate over every pages
        for page in pdf_reader.pages:
            #extract the text from every pages
            txt=page.extract_text()
            #clean the pdf 
            save=(re.sub(r"^\s+|\s+$", "", txt))
            #split the clean document into small small parts
            text_splitter = CharacterTextSplitter()
            docs = text_splitter.split_text(save)
            for i in range (len(docs)):
                chunk=docs[i]
                chunkInfo=(model.encode(chunk).tolist(),{'context': pdf})
                client.upsert(
                    collection_name="test_collection",
                    points= [PointStruct(
                        id = id,
                        vector = chunkInfo[i],
                        payload={'pdf':pdf}
                    )]
                )

        id+=1

    taken = time.time() - start
    print(f"Time taken for upload data to db: {taken:.2f} seconds.")     
    return render_template('index1.html', Files = os.listdir('./uploads'))
            
@app.route('/process_text', methods=['POST'])
def process_text():
    start = time.time()
    input = request.form["user_input"]
    query=model.encode(input).tolist()
    result=client.search(
                collection_name="test_collection",
                query_vector=query,
                limit=3)
    taken = time.time() - start
    print(f"Time taken for query search: {taken:.2f} seconds.")
    return render_template("result.html",result=result)


@app.route('/query', methods=['POST'])
def queryupload():
    start = time.time()
    if request.method == 'POST':
        file = request.files['file']
        file_path = "./queryresume/" + file.filename
        file.save(file_path)

        pdf_reader = PdfReader(file_path)
        for page in pdf_reader.pages:
            txt = page.extract_text()
            save = (re.sub(r"^\s+|\s+$", "", txt))
            text_splitter = CharacterTextSplitter()
            docs = text_splitter.split_text(save)
            query = (model.encode(docs).tolist())
            result = client.search(
                collection_name="test_collection",
                query_vector=query,
                limit=3
            )

        taken = time.time() - start
        print(f"Time taken for query search: {taken:.2f} seconds.")

        return render_template("result.html", result=result)


if __name__ == '__main__':
    app.run(debug=True)