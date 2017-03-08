#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import urllib.request
import urllib.parse
import os


def is_str(data=None):
    if isinstance(data, str):
        return True
    else:
        return False


def convert_to_address(latitude, longitude):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    keyid = os.environ.get('GOOGLE_API_KEY')
    latlng = str(latitude) + ',' +str(longitude)
    query = [
        ("format", "json"),
        ("latlng", latlng),
        ("key", keyid),
        ("language", 'ja')
    ]
    url += "?{0}".format(urllib.parse.urlencode(query))
    try:
        result = urllib.request.urlopen(url).read()
    except ValueError:
        print("APIアクセス失敗")
        sys.exit()
    data = json.loads(result.decode('utf-8'))
    address = data['results'][0]["formatted_address"]
    split_address = address.split(' ')
    address = ''
    for address_elem in split_address[2:]:
        address += address_elem
    if '丁目' in address:
        address = address.replace('丁目','-')
    return address

def create_url(latitude, longitude, offset):
    url = "https://api.gnavi.co.jp/RestSearchAPI/20150630/"
    keyid = os.environ.get('GURUNAVI_API_KEY')

    address = convert_to_address(latitude,longitude)
    #address = '神奈川県横浜市西区みなとみらい2-３'
    query = [
        ("format", "json"),
        ("keyid", keyid),
        ("address", address),
        ("offset", offset)
    ]
    url += "?{0}".format(urllib.parse.urlencode(query))
    return url

def get_data(latitude, longitude, offset):
    url = create_url(latitude, longitude, offset)
    result = send_requsest(url)
    data = json.loads(result.decode('utf-8'))
    if "error" in data:
        if "message" in data:
            print("{0}".format(data["message"]))
        else:
            print("データ取得に失敗しました。")
        sys.exit()
    if not "rest" in data:
        print("レストランデータが見つからなかったため終了します。")
        sys.exit()
    return data

def send_requsest(url):
    try:
        result = urllib.request.urlopen(url).read()
    except ValueError:
        print("APIアクセスに失敗しました。")
        sys.exit()
    return result

def show_total_hit(data):
    total_hit_count = None
    if "total_hit_count" in data:
        total_hit_count = data["total_hit_count"]

    if total_hit_count is None or int(total_hit_count) <= 0:
        print("指定した内容ではヒットしませんでした。")
        sys.exit()

    print("{0}件ヒットしました。".format(total_hit_count))
    print("----")
    return int(total_hit_count)


def narrow_shop_candidates(latitude, longitude, offset):
    data = get_data(latitude, longitude, offset)
    candidates = []
    append_count = 0
    total_hit_count = show_total_hit(data)

    while total_hit_count > 0:
        if append_count % 10 == 0:
            data = get_data(latitude, longitude, append_count)
        for shop_data in data['rest']:
            if total_hit_count == 0:
                break
            candidates.append(shop_data['name'])
            total_hit_count -= 1
            append_count += 1
    print(candidates)
    print(len(candidates))


if __name__ == '__main__':
    latitude = sys.argv[1]
    longitude = sys.argv[2]
    narrow_shop_candidates(latitude, longitude, 1)
    #narrow_shop_candidates(35.659272, 139.697958, 1)