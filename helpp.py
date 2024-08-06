import requests

import db
import db_redis
import net
from config import bot_url


# ==========================================================================================================================================

def get_bot_url(group_tg_id, typee=2):
    bot_url = db_redis.bot_url_get(group_tg_id, typee)
    if bot_url is None:
        bot_url = get_bot_url_default()
        
        bot = db.bot_one(group_tg_id, typee)
        if bot is None:
            return bot_url
            
        token = bot["token"]
        bot_url = "https://api.telegram.org/bot%s/" % token
        
        db_redis.bot_url_set(group_tg_id, typee, bot_url)

    return bot_url
    

def get_bot_url_default():
    return "https://api.telegram.org/bot6245957008:AAFlAhO2ULFioLWlYMddSHyV5W00lkW54os/" # qunguanBack

    
# ==========================================================================================================================================

def sendMessage(chat_id, text, btns=None):
    tg_url = bot_url + "sendMessage"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    if btns is not None:
        data["reply_markup"] = btns
    
    response = requests.post(tg_url, json=data, headers=headers, timeout=10)


def editMessageText(chat_id, message_id, text, btns=None):
    tg_url = bot_url + "editMessageText"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML",
    }
    
    if btns is not None:
        data["reply_markup"] = btns
    
    response = requests.post(tg_url, json=data, headers=headers, timeout=10)


def updateChatPhoto(chatId, photo):
    base_url = get_bot_url(chatId)

    flag, description = net.setChatPhotoRequest(base_url, chatId, photo)
    if flag == False:
        return False

    return True
