from flask import Flask, request, Response
import requests, json

app = Flask(__name__)
TARGET = "https://api.chaloapps.com"
RESOURCES = ['gold', 'coins', 'stars', 'diamonds', 'money', 'cash']
COLLECTIONS = ['weapons', 'guns', 'skins', 'suits', 'suits2', 'cars', 'hats', 'hairs', 'shoes', 'eyes', 'glasses', 'beak', 'backpack', 'items']

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    url = f"{TARGET}/{path}"
    resp = requests.request(
        method=request.method,
        url=url,
        headers={k: v for k, v in request.headers if k.lower() != 'host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    try:
        data = resp.json()
        for k in RESOURCES:
            if k in data: data[k] = 999999999
        for key in COLLECTIONS:
            if key in data and isinstance(data[key], list):
                for item in data[key]:
                    if isinstance(item, dict):
                        item['unlocked'] = True
                        item['price'] = 0
                        item['lvl'] = 0
        for ad in ['ads_enabled', 'placements']:
            if ad in data: data[ad] = False if ad == 'ads_enabled' else []
        data['__zeta'] = 'unlocked'
        modified = json.dumps(data)
    except:
        modified = resp.content
    headers = [(n, v) for n, v in resp.raw.headers.items() if n.lower() not in ['content-encoding', 'content-length', 'transfer-encoding', 'connection']]
    return Response(modified, resp.status_code, headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
