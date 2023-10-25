import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("mongodb+srv://lxtiara:admin@cluster0.zhgzgvs.mongodb.net/?retryWrites=true&w=majority")
DB_NAME =  os.environ.get("dbsparta")

connection_string = 'mongodb+srv://lxtiara:admin@cluster0.zhgzgvs.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string)
db = client.dbsparta

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/diary', methods=['GET'])
def show_diary():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})


@app.route('/diary', methods=['POST'])
def save_diary():
    # sample_receive =request.form.get('sample_give')
    # print(sample_receive)
    title_receive = request.form.get('title_give')

    # Kode agar user memasukan suatu nilai dalam box title atau description (server-side)
    # if title_receive == "":
    #     response = {"message": "Please enter the title of your image"}
    #     return jsonify(response)

    content_receive = request.form.get('content_give')
    # if content_receive == "":
    #     response = {"message": "Please enter some description"}
    #     return jsonify(response)
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    if 'file_give' in request.files:
        file = request.files['file_give']
        extension = file.filename.split('.')[-1]
        filename = f'static/post-{mytime}.{extension}'
        file.save(filename)
    else:
        # Gunakan gambar default jika input gambar kosong
        filename = 'static/default-image.jpg'

    if 'file_give' in request.files:
        profile = request.files['profile_give']
        extension = profile.filename.split('.')[-1]
        profilename = f'static/profile-{mytime}.{extension}'
        profile.save(profilename)
    else:
        # Gunakan gambar default jika input gambar kosong
        profilename = 'static/default-image.jpg'

    time = today.strftime('%Y.%m.%d')
    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive,
        'time': time
    }
    db.diary.insert_one(doc)

    return jsonify({'message': 'data was saved!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
