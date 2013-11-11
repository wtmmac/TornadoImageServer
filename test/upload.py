#/usr/bin/env python
# coding=utf-8
import time, hashlib

# pip install requests
import requests

url = 'http://localhost:8001/upload'

# 密钥
secret_key = "secret_key"

timestamp = int(time.time()).__str__()

sign = hashlib.md5(secret_key + timestamp).hexdigest().upper()

values = {'sign':sign, 'time':timestamp}

# image 
images = {'upload_image': open('hulu.jpg', 'rb')}

r = requests.post(url, data = values, files = images)

print r.text