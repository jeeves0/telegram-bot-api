import telegramBotAPI as api, time, flask, os

TOKEN = None #specify your code here if you want to run the code locally
app = flask.Flask(__name__)
mybot = api.bot(os.getenv("BOT_TOKEN", TOKEN))

if not TOKEN: mybot.setWebhook("https://"+os.environ["HEROKU_APP_NAME"]+".herokuapp.com/"+os.environ["BOT_TOKEN"])

def main(static):

	return static

def inlineQuery(static):

	return static

def inlineKeyboard(static):

	return static

@app.route("/"+os.getenv("BOT_TOKEN", TOKEN), methods=['POST'])
def bot_updates():

	mybot.new = api.objectify(flask.request.get_json())
	with open("data.json", "w") as staticFile:
		try:
			static = json.load(staticFile)
			if "callback_query" in mybot.new._fields:static = inlineKeyboard(static)
			elif "inline_query" in mybot.new._fields:static = inlineQuery(static)
			else:static = main(static)
		except Exception as e:print(e)
		json.dump(static, staticFile)
	return "200"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=os.getenv("PORT", 8080))