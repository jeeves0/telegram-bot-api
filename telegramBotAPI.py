import os, json, requests, collections

def objectify(obj): return json.loads(json.dumps(obj), object_hook=
    lambda d: collections.namedtuple('X', d.keys(), rename=True)(*d.values()))

class bot(object):
    """a class for interacting with the telegram bot"""
    def __init__(self, token):
        self.token = token
        self.new = None
        self.offset = 0

    class APIError(Exception):
        def __init__(self, error_code, description):
            self.error_code = error_code
            self.description = description
        def __str__(self):
            return f"{self.error_code}:{self.description}"
    
    def push(self, cmd, headers={}, debug=False, **kwargs):
        params = {key : val for key, val in kwargs.items()}
        res = requests.post("https://api.telegram.org/bot"+self.token+"/"+cmd, headers=headers, json=params).json()
        if debug:print("Command: %s\nParameters: %s\nResponse: %s" %(cmd, params, res))
        if res["ok"]: return objectify(res).result
        raise self.APIError(res["error_code"], res["description"])

    def getUpdates(self):
        x = bot.push(self, 'getUpdates', offset=self.offset, debug=False)
        if len(x):
            self.offset = x[0].update_id + 1
            self.new = x[0]
            return True
        return False

    def setWebhook(self, url):
        return bot.push(self, "setWebhook", url=url)

    def deleteWebhook(self):
        return bot.push(self, "setWebhook")

    def sendMessage(self, text, chat_id=None, **kwargs):
        return bot.push(self, "sendMessage", chat_id=chat_id if chat_id else self.new.message.chat.id, text=text, **kwargs)
            
    def answerInlineQuery(self, results, query_id=None, **kwargs):
        return bot.push(self, "answerInlineQuery", results=results, inline_query_id=query_id if query_id else self.new.inline_query.id, **kwargs)

    def answerCallbackQuery(self, query_id=None, **kwargs):
        return bot.push(self, "answerCallbackQuery", callback_query_id=query_id if query_id else self.new.callback_query.id, **kwargs)

    def getChatMember(self, chat_id, user_id):
        return bot.push(self, "getChatMember", chat_id=chat_id, user_id=user_id)

    def editMessageText(self, text, **kwargs):
        return bot.push(self, "editMessageText", text=text, **kwargs)

    def editMessageReplyMarkup(self, **kwargs):
        return bot.push(self, "editMessageReplyMarkup", **kwargs)

class reply_markup(object):
    """docstring for keyboard"""
    class inline(object):
        """docstring for inline"""
        def __init__(self):
            self.keyboard = {"inline_keyboard": []}

        def add(self, text, row=None, col=None, **kwargs):
            button = {"text": text, **kwargs}
            if not row or row >= len(self.keyboard["inline_keyboard"]):self.keyboard["inline_keyboard"].append([button])
            elif not col or col >= len(self.keyboard["inline_keyboard"][row]):self.keyboard["inline_keyboard"][row].append(button)
            else:self.keyboard["inline_keyboard"][row].insert(col, button)
            return button

    class reply(object):
        """docstring for reply"""
        def __init__(self, **kwargs):
            self.keyboard = {"reply_keyboard":[], **kwargs}

        def add(self, text, row=None, col=None, **kwargs):
            button = {"text": text, **kwargs}
            if not row or row >= len(self.keyboard["reply_keyboard"]):self.keyboard["reply_keyboard"].append([button])
            elif not col or col >= len(self.keyboard["reply_keyboard"][row]):self.keyboard["reply_keyboard"][row].append(button)
            else:self.keyboard["reply_keyboard"][row].insert(col, button)
            return button

    class remove(object):
        """docstring for remove"""
        def __init__(self, selective=False):
            self.keyboard = {"remove_keyboard": True, "selective": selective}

def inlineQueryResult(res_type, res_id, **kwargs):
    return {"type": res_type, "id": res_id, **kwargs}
