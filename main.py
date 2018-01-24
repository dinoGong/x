# -*- coding: utf-8 -*-
import os
from flask import Flask, request, redirect, url_for,render_template,session,send_from_directory,jsonify,escape
from werkzeug.utils import secure_filename
import requests
import json
from urllib import parse
UPLOAD_FOLDER = os.path.dirname(os.path.abspath('static'))+'/static/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.secret_key = 'akjdfkajdkfakdjfjahdfkasdfjahsdjfasjkfjads'


access_token="24.a31a91c67186684f28fe8a4ebd6173df.2592000.1519374568.282335-10738303" # 以后可以写在配置里，并制定一个为期30天的定时任务，每30天重新获取一次access_token

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file',filename=filename))
            img_url=url_for('static',filename=filename)
            #return jsonify(img=img_url)
            return img_url
    return render_template('upload.html',title="uploadServer")
@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('default.html',title="x",logged=True,username=session['username'])
    return render_template('default.html',title="x",logged=False)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template('login.html',title="Login")

@app.route('/login_with_face',methods=['GET','POST'])
def login_with_face():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template('login_with_face.html',title="Login")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404



# api
#detect 人脸检测
@app.route('/api/detect',methods=['GET','POST'])
def api_detect():
    if request.method == 'POST':
        img_base64=request.form['img_base64']
        request_url = "https://aip.baidubce.com/rest/2.0/face/v1/detect"
        params = {"face_fields":"age,beauty,expression,faceshape,gender,glasses,landmark,race,qualities","image":img_base64,"max_face_num":5}
        request_url = request_url + "?access_token=" + access_token
        params=parse.urlencode(params)
        #s = json.dumps(params)
        r = requests.post(request_url, data=params)
        return jsonify(r.json())
    return render_template('/api/detect.html',title="api:detect")


if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=3000)
