import telegramBotAPI as api, time, flask, os, sys, requests, signal, json
from box import Box

TOKEN = None # Telegran Bot Token
jsonBinId = None # JSONBin Bin Id 
jsonMasterKey = None # JSONBin API Key

app = flask.Flask(__name__)
mybot = api.bot(os.getenv("BOT_TOKEN", TOKEN))
static = Box(requests.get("https://api.jsonbin.io/v3/b/"+jsonBinId+"/latest", headers={"X-MASTER-KEY": jsonMasterKey}).json()["record"])

def onSIG(signum, frame):
	
	requests.put("https://api.jsonbin.io/v3/b/"+jsonBinId, headers={"X-MASTER-KEY": jsonMasterKey}, json=static)
	sys.exit()

signal.signal(signal.SIGINT, onSIG)
signal.signal(signal.SIGTERM, onSIG)

if os.getenv("BOT_TOKEN", None): mybot.setWebhook("https://"+os.environ["HEROKU_APP_NAME"]+".herokuapp.com/"+os.environ["BOT_TOKEN"])
else: mybot.deleteWebhook()

def main(static):

	return static

def inlineQuery(static):

	return static

def inlineKeyboard(static):

	return static

@app.route("/"+os.getenv("BOT_TOKEN", TOKEN), methods=['POST'])
def bot_updates():

	global static
	if os.getenv("BOT_TOKEN", None):
		mybot.new = api.objectify(flask.request.get_json())

	try:
		if "callback_query" in mybot.new._fields:
			mybot.new = mybot.new.callback_query
			static = inlineKeyboard(static)

		elif "inline_query" in mybot.new._fields:
			mybot.new = mybot.new.inline_query
			static = inlineQuery(static)

		elif "message" in mybot.new._fields:
			mybot.new = mybot.new.message
			static = main(static)

	except Exception as e:
		print(f"Line {e.__traceback__.tb_lineno}: {e}")

	return "200"

if __name__ == "__main__":
	if os.getenv("BOT_TOKEN", None):
		app.run(host="0.0.0.0", port=os.getenv("PORT", 8080))
	else:
		print("Long polling started...")
		while True:
			if mybot.getUpdates():
				updateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				tmp = time.time()
				bot_updates()
				print(f"[{updateTime}]: {time.time() - tmp}")
			else:time.sleep(3)