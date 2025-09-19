import json
import os
from dotenv import load_dotenv
import urllib.parse
import hashlib
import requests
from pathlib import Path
import time


load_dotenv()
public = os.getenv("PUBLIC_KEY")
private = os.getenv("PRIVATE_KEY")
#print(public, private)
BASE = "https://gateway.marvel.com/v1/public"
COMICS = 'comics'

SPIDERMAN = "https://gateway.marvel.com/v1/public/characters/1009610/comics"
BASE2 = "https://gateway.marvel.com/v1/public/characters/1009610/comics"
BASE3 = "https://gateway.marvel.com/v1/public/comics/6891/"
def auth_hash(ts, public, private):
    text = f'{ts}{private}{public}'
    hash_result = hashlib.md5(text.encode()).hexdigest()
    return hash_result


def get_comics():
    response = make_request(100, 50000, '1', "https://gateway.marvel.com/v1/public/comics/")
    return extract_json(response)


def make_request(limit, offset, ts, url):
    
    params = {'ts': ts, 'apikey' : public, 'hash':auth_hash(ts, public, private), 'limit': limit, 'offset': offset}
    
    response = requests.get(url, params)
    print(response.url)
    if response.status_code == 200:
        return response
    else:
        print(response.json(), "Something went wrong.")
        

def extract_json(response):
    data = response.json()
    return data

def write_json_data(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent = 2) 


def main():

    ts = 1 
    total_issues = 4599
    end = 401    
    for off in range(0, end, 100):
        resp = make_request(100, off, ts)
        json_data = extract_json(resp)
        write_json_data(json_data, Path('.')/f'comics{ts}.json')
        ts += 1 
        time.sleep(3)
        print(off)
        

if __name__ == '__main__':
    d = get_comics()
    write_json_data(d, Path('.')/f'test{5}.json')
    print(d)



'''
if __name__ == '__main__':
    url = f'{BASE3}'
    params = {}
    ts = "1" 
    
    params['ts'] = ts
    params['apikey'] = public
    params['hash'] = auth_hash(ts, public, private)
    params['limit']=100
    params['offset']=40
    response = requests.get(url, params)
   # print(response.url)
    #print(response.json())
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data))
    else:
        print(response.status_code, "something went wrong")

'''