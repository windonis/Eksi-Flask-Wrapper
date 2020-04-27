from flask import Flask
import requests
from lxml import html
import json
from flask import jsonify
from flask_cors import CORS
allTopic = []


def parse_eksi(url):
    headers = requests.utils.default_headers()
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    r = requests.get(url, headers=headers)
    return r

def find_titles():
    r = parse_eksi(url="https://eksisozluk.com/basliklar/m/populer?p=1")
    tree = html.fromstring(r.content)
    test = (tree.xpath('//a/@href'))
    for i in test:
        if "a=popular" in i:
            allTopic.append(i)
    return allTopic

def find_best(part):
    part = part.replace("popular","nice")
    url = "https://eksisozluk.com/" + part
    r = parse_eksi(url=url)
    tree = html.fromstring(r.content)
    entry_array = ''
    entry = (tree.xpath('/html/body/div[2]/div[2]/div[2]/section/div/ul/li[1]/div[1]/text()'))
    yazar = (tree.xpath('/html/body/div[2]/div[2]/div[2]/section/div/ul/li[1]/@data-author'))
    fav = (tree.xpath('/html/body/div[2]/div[2]/div[2]/section/div/ul/li[1]/@data-favorite-count'))
    tarih = (tree.xpath('/html/body/div[2]/div[2]/div[2]/section/div/ul/li[1]/footer/div[2]/a[1]/text()'))
    id_entry = (tree.xpath('/html/body/div[2]/div[2]/div[2]/section/div/ul/li[1]/@data-id'))
    entry_link = "https://eksisozluk.com/entry/" + id_entry[0]

    for i in entry:
        entry_array = entry_array + i
    try:
        python_object = { "id_entry": id_entry,"yazar":yazar,"fav": fav,"tarih": tarih,"entry": entry_array, "konu":entry_link }
    except:
        print("sorun yok desvam")
    return python_object

app = Flask(__name__)

@app.route('/')
def run_all():
    allTopic = find_titles()
    total = []
    for i in allTopic:
        total.append(find_best(i))
    allTopic.clear()
    response = jsonify(total)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run()
