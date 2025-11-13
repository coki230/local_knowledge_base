from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/query', methods=['POST'])
def query_file():
    data = request.get_json()
    file_path = data.get('path', '').strip()

    if not file_path:
        return jsonify({'error': 'Please enter a file path'}), 400

    # Security check: prevent directory traversal
    if '..' in file_path or file_path.startswith('/proc'):
        return jsonify({'error': 'Access to this path is not allowed'}), 403

    try:
        if not os.path.exists(file_path):
            return jsonify({'error': 'File or path does not exist'}), 404

        if not os.path.isfile(file_path):
            return jsonify({'error': 'Path exists but it is not a file'}), 400

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return jsonify({'content': content})

    except PermissionError:
        return jsonify({'error': 'Permission denied to read this file'}), 403
    except Exception as e:
        return jsonify({'error': f'Failed to read file: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
