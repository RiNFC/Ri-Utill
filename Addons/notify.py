import requests

def notify(content, title):
    url = 'http://127.0.0.1:5766/notify'
    data = {'content': content, "title": title}
    resp = requests.post(url, data=data)
    return(resp.status_code)