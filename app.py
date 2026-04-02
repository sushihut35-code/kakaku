from flask import Flask, jsonify, request, send_from_directory
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE_DIR)

DATA_FILE = os.path.join(BASE_DIR, 'data.json')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        default_data = {
            "suppliers": [
                {
                    "name": "山口水産",
                    "products": [
                        {"name": "刺身盛り合わせ", "price": 1500},
                        {"name": "焼き魚セット", "price": 800},
                        {"name": "寿司セット", "price": 2000}
                    ]
                },
                {
                    "name": "田中青果",
                    "products": [
                        {"name": "季節野菜セット", "price": 500},
                        {"name": "フルーツ盛り", "price": 1200}
                    ]
                }
            ]
        }
        save_data(default_data)
        return default_data

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(load_data())

@app.route('/api/data', methods=['POST'])
def update_data():
    data = request.json
    save_data(data)
    return jsonify({'success': True})

if __name__ == '__main__':
    print('サーバーを起動しました...')
    print(f'PC: http://localhost:8080')
    print(f'スマホ: http://192.168.68.56:8080')
    app.run(host='0.0.0.0', port=8080, debug=False)
