from flask import Flask, jsonify, request, send_from_directory
import requests as http_req
import json
import os
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE_DIR)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://bsgfragmulyurahonkle.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_fHE_lHb3Ma4g0SVlyBtv2w_SH-MZ-Tf")

DEFAULT_DATA = {
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


def sb_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }


def utc_now():
    return datetime.now(timezone.utc).isoformat()


@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)


@app.route('/api/data', methods=['GET'])
def get_data():
    if not SUPABASE_URL:
        return jsonify({"data": DEFAULT_DATA, "updated_at": None})
    try:
        resp = http_req.get(
            f"{SUPABASE_URL}/rest/v1/app_data?id=eq.1&select=data,updated_at",
            headers=sb_headers()
        )
        resp.raise_for_status()
        rows = resp.json()
        if rows:
            return jsonify({"data": rows[0]["data"], "updated_at": rows[0]["updated_at"]})
    except Exception as e:
        print(f"GET error: {e}")
    return jsonify({"data": DEFAULT_DATA, "updated_at": None})


@app.route('/api/data', methods=['POST'])
def update_data():
    payload = request.json
    updated_at = utc_now()
    if not SUPABASE_URL:
        return jsonify({'success': False, 'error': 'No Supabase config'}), 500
    try:
        resp = http_req.patch(
            f"{SUPABASE_URL}/rest/v1/app_data?id=eq.1",
            headers=sb_headers(),
            json={"data": payload, "updated_at": updated_at}
        )
        resp.raise_for_status()
        return jsonify({'success': True, 'updated_at': updated_at})
    except Exception as e:
        print(f"POST error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print('サーバーを起動しました...')
    print(f'PC: http://localhost:8080')
    print(f'スマホ: http://192.168.68.56:8080')
    app.run(host='0.0.0.0', port=8080, debug=False)
