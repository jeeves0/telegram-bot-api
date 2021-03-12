import os, json, requests
from telethon import utils
from box import Box

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
        res = Box(requests.post("https://api.telegram.org/bot"+self.token+"/"+cmd, headers=headers, json=params).json())
        if debug:print("Command: %s\nParameters: %s\nResponse: %s" %(cmd, params, res))
        if res.ok: return res.result
        raise self.APIError(res.error_code, res.description)

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

    def getChat(self, chat_id):
        return self.push("getChat", chat_id=chat_id)

    def getChatMember(self, chat_id=None, user_id=None):
        return self.push("getChat", chat_id=chat_id if chat_id else self.new.chat.id, user_id=user_id if user_id else self.new.xfrom.id)

    def setWebhook(self, url):
        return self.push("setWebhook", url=url)

    def deleteWebhook(self):
        return self.push("setWebhook")

    def sendMessage(self, text, chat_id=None, **kwargs):
        return self.push("sendMessage", chat_id=chat_id if chat_id else self.new.chat.id, text=text, **kwargs)
            
    def answerInlineQuery(self, results, query_id=None, **kwargs):
        return self.push("answerInlineQuery", results=results, inline_query_id=query_id if query_id else self.new.id, **kwargs)

    def answerCallbackQuery(self, query_id=None, **kwargs):
        return self.push("answerCallbackQuery", callback_query_id=query_id if query_id else self.new.id, **kwargs)

    def getChatMember(self, chat_id=None, user_id=None):
        return self.push("getChatMember", chat_id=chat_id if chat_id else self.new.chat.id, user_id=user_id if user_id else self.new.xfrom.id)

    def editMessageText(self, text, **kwargs):
        return self.push("editMessageText", text=text, **kwargs)

    def editMessageReplyMarkup(self, **kwargs):
        return self.push("editMessageReplyMarkup", **kwargs)

    def copyMessage(self, message_id, from_chat_id, chat_id=None, **kwargs):
        return self.push("copyMessage", message_id=message_id, from_chat_id=from_chat_id, chat_id=chat_id if chat_id else self.new.chat.id, **kwargs)

    def forwardMessage(self, message_id, from_chat_id, chat_id=None, **kwargs):
        return self.push("forwardMessage", message_id=message_id, from_chat_id=from_chat_id, chat_id=chat_id if chat_id else self.new.chat.id, **kwargs)

    def deleteMessage(self, message_id=None, chat_id=None):
        return self.push("deleteMessage", message_id=message_id if message_id else self.new.message_id, chat_id=chat_id if chat_id else self.new.chat.id)

    def editMessageReplyMarkup(self, **kwargs):
        return self.push("editMessageReplyMarkup", **kwargs)

    def pinChatMessage(self, chat_id=None, message_id=None, **kwargs):
        return self.push("pinChatMessage", chat_id=chat_id if chat_id else self.new.chat.id, message_id=message_id if message_id else self.new.message_id, **kwargs)

class reply_markup(object):
    """docstring for keyboard"""
    class inline(object):
        """docstring for inline"""
        def __init__(self):
            self.keyboard = {"inline_keyboard": []}

        def add(self, text, row=0, col=69420, **kwargs):
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
