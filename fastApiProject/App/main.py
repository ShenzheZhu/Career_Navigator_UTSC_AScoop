import io

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
import os

from App.dependency import recommender_execute, get_job_details
from algorithm.algorithms import Neo4jRecommender
from pipelines.resume_pipeline.resume_processing_gemini import ResumeAnalyzerGemini
from resources import config, cloud_config


app = Flask(__name__)

# Specify the directory where files will be saved
UPLOAD_DIRECTORY = config.LOCAL_RESUME_BUCKET
app.secret_key = "bbd30619de971f981815988979b2b23ffebc8ed4758bf9c5"


@app.route('/')
def index():
    error = request.args.get('error', '')
    return render_template('index.html', error=error)


@app.route('/trial')
def trial():
    return render_template('trial.html')

@app.route('/result')
def result():
    return render_template('result.html')




@app.route('/upload', methods=['POST'])
def upload_file():
    # 检查是否有文件部分在请求中
    if 'file' not in request.files:
        return jsonify({'error': "No file part in the request."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': "No file selected."}), 400

    filename = secure_filename(file.filename)
    file_stream = io.BytesIO(file.read())  # 读取文件到内存

    results = recommender_execute(file_stream)  # 假设这是处理文件并返回结果的函数

    if results:
        enhanced_results = [get_job_details(result) for result in results]
        print(enhanced_results)
        return jsonify({'results': enhanced_results})
    else:
        return jsonify({'error': "No results available or an error occurred."}), 404


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in {'pdf'}


if __name__ == '__main__':
    app.run(debug=True)
