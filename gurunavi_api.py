#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib.request
import json


def is_str(data=None):
    if isinstance(data, str):
        return True
    else:
        return False


keyid = "ab49331ac199361e2a76b0248d49add2"
url = "https://api.gnavi.co.jp/RestSearchAPI/20150630/"
latitude = "35.659272"
longitude = "139.697958"
range = "1"

query = [
    ("format", "json"),
    ("keyid", keyid),
    ("latitude", latitude),
    ("longitude", longitude),
    ("range", range)
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

disp_count = 0

for rest in data["rest"]:
    line = []
    id = ""
    name = ""
    code_category_name_s = []
    # 店舗番号
    if "id" in rest and is_str(rest["id"]):
        id = rest["id"]
    line.append(id)
    # 店舗名
    if "name" in rest and is_str(rest["name"]):
        name = u"{0}".format(rest["name"])
    line.append(name)
    if "access" in rest:
        access = rest["access"]
        # 最寄の路線
        if "line" in access and is_str(access["line"]):
            access_line = u"{0}".format(access["line"])
        # 最寄の駅
        if "station" in access and is_str(access["station"]):
            access_station = u"{0}".format(access["station"])
        # 最寄駅から店までの時間
        if "walk" in access and is_str(access["walk"]):
            access_walk = u"{0}分".format(access["walk"])
    line.extend([access_line, access_station, access_walk])
    # 店舗の小業態
    if "code" in rest and "category_name_s" in rest["code"]:
        for category_name_s in rest["code"]["category_name_s"]:
            if is_str(category_name_s):
                code_category_name_s.append(u"{0}".format(category_name_s))
    line.extend(code_category_name_s)
    # タブ区切りで出力
    print("\t".join(line))
    disp_count += 1

# 出力件数を表示して終了
print("----")
print("{0}件出力しました。".format(disp_count))
sys.exit()