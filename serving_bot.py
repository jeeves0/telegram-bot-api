import requests, time, json

update = 0
offset = 0
TOKEN = "YOUR_BOT_TOKEN_HERE"
delay = 3

def x():return requests.post("https://api.telegram.org/bot"+TOKEN+"/getUpdates", json={"offset": offset}).json()

while True:
    try:
        temp = x()
        offset = temp["result"][0]["update_id"]
        update = temp["result"][-1]
        requests.post("http://localhost:8080/"+TOKEN, json=update)
        break
    except:time.sleep(delay)
while True:
    try:
        temp = x()
        if temp["result"][-1] != update:
            update = temp["result"][-1]
            offset += 1
            requests.post("http://localhost:8080/"+TOKEN, json=update)
    except:pass
    time.sleep(delay)
