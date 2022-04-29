import json

def send_json(dic):
    with open('../output_json/out.json','w') as out:
        json.dump(dic, out, indent=4)

    x = 1