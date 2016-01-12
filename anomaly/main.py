# coding: utf-8

feature_type = []

with open("./data/kddcup.names", "r") as f:
    f.readline()
    while True:
        line = f.readline().rstrip()
        if line == "":
            break
        # 特徴名とタイプを分ける
        feature_type.append(line.split(": "))

data = []
with open("./data/kddcup.data.csv", "r") as f:
    while True:
        line = f.readline().rstrip()
        if line == "":
            break
        features = {}
        for schema, value in zip(feature_type, line.split(",")):
            fname, ftype = schema
            if ftype == "continuous.":
                features[fname] = float(value)
            elif ftype == "symbolic.":
                features[fname] = value
            else:
                assert(not "unknown type")
        # print features
        data.append(features)

import jubatus
from jubatus.common import Datum

client = jubatus.Anomaly("127.0.0.1", 9199, "kdd")
for datum in data:
    result = client.add(Datum(datum)).score
    if 2.0 < result:
        print (str(datum) + "is anomaly!")
