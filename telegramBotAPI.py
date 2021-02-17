import os, json, requests, collections
from telethon import utils

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
        x = self.push('getUpdates', offset=self.offset, debug=False)
        if len(x):
            self.offset = x[0].update_id + 1
            self.new = x[0]
            return True
        return False

    def getMe(self):
        return self.push("getMe")

    def getChatFromLink(self, link):
        return utils.resolve_invite_link(link)[1]

    def setWebhook(self, url):
        return self.push("setWebhook", url=url)

    def deleteWebhook(self):
        return self.push("setWebhook")

    def sendMessage(self, text, chat_id=None, **kwargs):
        return self.push("sendMessage", chat_id=chat_id if chat_id else self.new.message.chat.id, text=text, **kwargs)
            
    def answerInlineQuery(self, results, query_id=None, **kwargs):
        return self.push("answerInlineQuery", results=results, inline_query_id=query_id if query_id else self.new.inline_query.id, **kwargs)

    def answerCallbackQuery(self, query_id=None, **kwargs):
        return self.push("answerCallbackQuery", callback_query_id=query_id if query_id else self.new.callback_query.id, **kwargs)

    def getChatMember(self, chat_id, user_id):
        return self.push("getChatMember", chat_id=chat_id, user_id=user_id)

    def editMessageText(self, text, **kwargs):
        return self.push("editMessageText", text=text, **kwargs)

    def editMessageReplyMarkup(self, **kwargs):
        return self.push("editMessageReplyMarkup", **kwargs)

class reply_markup(object):
    """docstring for keyboard"""
    class inline(object):
        """docstring for inline"""
        def __init__(self):
            self.keyboard = {"inline_keyboard": []}

        def add(self, text, row=0, col=0, **kwargs):
            button = {"text": text, **kwargs}
            if row >= len(self.keyboard["inline_keyboard"]):self.keyboard["inline_keyboard"].append([button])
            elif col >= len(self.keyboard["inline_keyboard"][row]):self.keyboard["inline_keyboard"][row].append(button)
            else:self.keyboard["inline_keyboard"][row].insert(col, button)
            return button

    class reply(object):
        """docstring for reply"""
        def __init__(self, **kwargs):
            self.keyboard = {"keyboard":[], **kwargs}

        def add(self, text, row=0, col=69420, **kwargs):
            button = {"text": text, **kwargs}
            if row >= len(self.keyboard["keyboard"]):self.keyboard["keyboard"].append([button])
            elif col >= len(self.keyboard["keyboard"][row]):self.keyboard["keyboard"][row].append(button)
            else:self.keyboard["keyboard"][row].insert(col, button)
            return button

    class remove(object):
        """docstring for remove"""
        def __init__(self, selective=False):
            self.keyboard = {"remove_keyboard": True, "selective": selective}

def inlineQueryResult(res_type, res_id, **kwargs):
    return {"type": res_type, "id": res_id, **kwargs}
