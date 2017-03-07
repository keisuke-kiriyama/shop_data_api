#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import urllib.request
import urllib.parse


def is_str(data=None):
    if isinstance(data, str):
        return True
    else:
        return False


def convert_to_address(latitude, longitude):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    keyid = 'AIzaSyDtqR5cHQQhd3maSOgUUTDHJjbIgHmaORs'
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
    return address


def narrow_shop_candidates(latitude, longitude):
    url = "https://api.gnavi.co.jp/RestSearchAPI/20150630/"
    keyid = "ab49331ac199361e2a76b0248d49add2"
    #address = convert_to_address(latitude,longitude)
    address = '神奈川県横浜市西区みなとみらい2-2-1'
    query = [
        ("format", "json"),
        ("keyid", keyid),
        ("address", address)
    ]
    url += "?{0}".format(urllib.parse.urlencode(query))
    try:
        result = urllib.request.urlopen(url).read()
    except ValueError:
        print("APIアクセスに失敗しました。")
        sys.exit()
    data = json.loads(result.decode('utf-8'))

    if "error" in data:
        if "message" in data:
            print("{0}".format(data["message"]))
        else:
            print("データ取得に失敗しました。")
        sys.exit()

    total_hit_count = None
    if "total_hit_count" in data:
        total_hit_count = data["total_hit_count"]

    if total_hit_count is None or int(total_hit_count) <= 0:
        print("指定した内容ではヒットしませんでした。")
        sys.exit()

    if not "rest" in data:
        print("レストランデータが見つからなかったため終了します。")
        sys.exit()

    print("{0}件ヒットしました。".format(total_hit_count))
    print("----")

    candidates = []
    print(len(data['rest']))
    for shop_data in data['rest']:
        candidates.append(shop_data['name'])

    print(candidates)
    #print(json.dumps(data, ensure_ascii=False, indent=2))


narrow_shop_candidates(35.659272, 139.697958)