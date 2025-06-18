from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
API_KEY = os.environ.get('OPENCELLID_API_KEY', 'pk.cbcb78f7f60d07fa5820220da051cdad')

@app.route('/api/lookup', methods=['GET'])
def lookup():
    phone = request.args.get('phone')
    mcc = request.args.get('mcc')
    mnc = request.args.get('mnc')
    lac = request.args.get('lac')
    cellid = request.args.get('cellid')
    if not all([phone, mcc, mnc, lac, cellid]):
        return jsonify({'error': 'Missing parameters'}), 400
    try:
        res = requests.get(
            f'https://opencellid.org/cell/get?key={API_KEY}&mcc={mcc}&mnc={mnc}&lac={lac}&cellid={cellid}&format=json'
        )
        data = res.json()
        return jsonify({
            'phone': phone,
            'mcc': mcc, 'mnc': mnc, 'lac': lac, 'cellid': cellid,
            'lat': data.get('lat'), 'lon': data.get('lon'),
            'range': data.get('range'), 'samples': data.get('samples'),
            'address': data.get('address', 'N/A')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
