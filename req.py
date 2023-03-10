import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)

url = 'https://localhost:8080/'
print("with client cert")
response = requests.get(url,  cert=('client-cert.pem', 'client-key.pem'), verify='ca-cert.pem')
print(response.text)
print("without client cert")
try:
    response = requests.get(url,   verify='ca-cert.pem')
    print('sucess')
except:
    print('failed')