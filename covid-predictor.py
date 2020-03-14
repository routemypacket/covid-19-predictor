# !/usr/bin/env/python3
import json

with open('./data/covid.json') as f:
  data = json.load(f)

#x = thisdict["model"]

#x = thisdict.get("model")

for x,y in data.items():
    print(x,y)
