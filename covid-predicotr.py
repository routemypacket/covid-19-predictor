# !/usr/bin/env/python3


italy = {
  "feb20" : {
    "cases" : 4,
  },
  "feb21" : { 
    "cases" : 21,
  },
  "feb22" : { 
    "cases" : 79,
  },
  "feb23" : { 
    "cases" : 157,
  },
  "feb24" : { 
    "cases" : 229,
  },
  "feb25" : { 
    "cases" : 323,
  },
  "feb26" : { 
    "cases" : 470,
  },
} 

with open('./data/covid.json') as f:
  data = json.load(f)

#x = thisdict["model"]

#x = thisdict.get("model")

for x,y in italy.items():
    print(x,y)
