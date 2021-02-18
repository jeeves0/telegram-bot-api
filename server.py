import telegramBotAPI as api, time, flask, os

TOKEN = None #specify your code here if you want to run the code locally
app = flask.Flask(__name__)
mybot = api.bot(os.getenv("BOT_TOKEN", TOKEN))

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

	mybot.new = api.objectify(flask.request.get_json())
	#print(mybot.new)
	try:
		with open("data.json", "r") as static:
			currStatic = json.load(static)
	except json.decoder.JSONDecodeError, FileNotFoundError:
		currStatic = {} #Default JSON to use if JSON file not found, corrupted or had invalid syntax

	if "callback_query" in mybot.new._fields:newStatic = inlineKeyboard(currStatic)
	elif "inline_query" in mybot.new._fields:newStatic = inlineQuery(currStatic)
	else:newStatic = main(currStatic)
	
	with open("data.json", "w") as static:
		json.dump(newStatic, static)

	return "200"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=os.getenv("PORT", 8080))