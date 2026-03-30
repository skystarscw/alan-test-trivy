# 支付系统 API - 正式版本 v2.0.0
import hashlib
import json
from flask import Flask, request

app = Flask(__name__)

def verify_signature(data, signature):
    """验证支付请求签名"""
    expected = hashlib.sha256(json.dumps(data).encode()).hexdigest()
    return expected == signature

@app.route('/api/payment', methods=['POST'])
def process_payment():
    data = request.json
    signature = request.headers.get('X-Signature')
    
    if not verify_signature(data, signature):
        return {'error': '签名验证失败'}, 401
    
    amount = data.get('amount')
    card = data.get('card_number')
    
    print(f"处理支付: {amount} 元, 卡号: {card[-4:]}")
    
    return {'status': 'success', 'transaction_id': 'TXN123456'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
