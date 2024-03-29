from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

Connection_string = 'mongodb+srv://Tirtayudha:tyo@cluster1.wqoczbh.mongodb.net/'
client = MongoClient(Connection_string)
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
    # sample_receive = request.form.get('sample_give')
    # print(sample_receive)
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)

    profil = request.files['profil_give']
    extension = profil.filename.split('.')[-1]
    profilname = f'static/profil-{mytime}.{extension}'
    profil.save(profilname)


    doc = {
        'file': filename,
        'profil': profilname,
        'title': title_receive,
        'content': content_receive
    }
    db.diary.insert_one(doc)
    return jsonify({'message': 'data sudah tersimpan'})
     
# untuk save mulai dari atas
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

