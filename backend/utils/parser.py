import requests

def parser(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        raise ValueError(response.status_code)