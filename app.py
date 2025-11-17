from flask import Flask, render_template, request, jsonify
import os
from util import init_llm, retrieve_language

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/initialize', methods=['POST'])
def initialize():
    data = request.get_json()
    file_path = data.get('path', '').strip()
    lang = data.get('language', 'en')  # 'en' or 'zh'

    if not file_path:
        return jsonify({'error': 'File path is required'}), 400

    if '..' in file_path:
        return jsonify({'error': 'Invalid path'}), 403

    try:
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        init_llm(file_path, lang)

        return jsonify({'status': 'success', 'message': 'Initialized successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/query', methods=['POST'])
def query():

    data = request.get_json()
    question = data.get('question', '').lower()

    # 简单模拟回答（你可以替换成调用大模型或检索逻辑）
    answer = retrieve_language(question)

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
