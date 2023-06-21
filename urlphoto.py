import requests
import json

def take_purl():
    info = dict()
    url = "https://api.unsplash.com//photos/random?client_id="
    r = requests.get(url=url)
    data = json.loads(r.text)
    info['url'] = data['urls']['small']
    info['autor'] = data['user']['name']
    info['caption'] = data['alt_description']
    return(info)

# print(take_purl())