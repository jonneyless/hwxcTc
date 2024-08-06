import json
import time

import requests
from retrying import retry

headers_tg = {
    "Content-Type": "application/json",
}

description_arr = [
    "Forbidden: bot was blocked by the user",
    "Forbidden: bot was kicked from the group chat",
    "Forbidden: bot was kicked from the supergroup chat",
    "Bad Request: not enough rights to send text messages to the chat",
    "Bad Request: message to delete not found",
    "Bad Request: chat not found",
    "Bad Request: group chat was upgraded to a supergroup chat",
]
   
# ============================================================================================================================================

def getDeleteMessagesRetry(result):
    flag = result[0]
    description = result[1]
    
    if flag is None:
        print("getDeleteMessagesRetry: %s" % description)
        return True
    else:
        return False
        
        
def deleteMessagesWrap(bot_url, chat_id, message_ids):
    description = ""
    
    try:
        return deleteMessages(bot_url, chat_id, message_ids)
    except Exception as e:
        description = e
        print("deleteMessagesWrap Exception: %s" % e)
    
    return None, description
        
        
@retry(stop_max_attempt_number=3, retry_on_result=getDeleteMessagesRetry)
def deleteMessages(bot_url, chat_id, message_ids):
    tg_url = bot_url + "deleteMessages"
    
    headers = headers_tg
    
    data = {
        "chat_id": chat_id,
        "message_ids": json.dumps(message_ids),
    }
    
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("deleteMessages Exception: %s" % e)
    
    if response is None:
        return None, "requests error"
    
    flag = False
    description = ""
    
    # flag = False 删除失败，不需要重试：信息已不存在
    # flag = True 删除成功，不需要重试
    # flag = None 删除失败，需要重试：tg异常，tg限制
    
    if response is not None:
        response_text = json.loads(response.text)
        # print(response_text)
        print("delete %s %s %s" % (chat_id, len(message_ids), response_text))

        if "ok" in response_text:
            if response_text["ok"]:
                flag = True
            else:
                description = ""
                if "description" in response_text:
                    description = response_text["description"]
                
                if description in description_arr:
                    # 不用重试
                    flag = False
                
                if "error_code" in response_text:
                    error_code = str(response_text["error_code"])
                    
                    if error_code == "429":
                        if "parameters" in response_text and "retry_after" in response_text["parameters"]:
                            retry_after = int(response_text["parameters"]["retry_after"])
                            print("deleteMessage sleep %s" % retry_after)
                            time.sleep(retry_after)
                            # 需要重试
                            flag = None
                    elif error_code == "403":
                        pass
        else:
            # tg异常重试
            flag = None
            description = "tg error"
    
    return flag, description
    

# ============================================================================================================================================
    
def getBanChatMemberRetry(result):
    flag = result[0]
    description = result[1]
    
    if flag is None:
        print("getBanChatMemberRetry: %s" % description)
        return True
    else:
        return False
        
        
def banChatMemberWrap(bot_url, chat_id, user_id):
    description = ""
    
    try:
        return banChatMember(bot_url, chat_id, user_id)
    except Exception as e:
        description = e
        print("banChatMemberWrap Exception: %s" % e)
    
    return None, description
        
        
@retry(stop_max_attempt_number=3, retry_on_result=getBanChatMemberRetry)
def banChatMember(bot_url, chat_id, user_id):
    tg_url = bot_url + "banChatMember"
    
    headers = headers_tg
    
    data = {
        "chat_id": chat_id,
        "user_id": user_id,
    }
    
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("banChatMember Exception: %s" % e)
    
    if response is None:
        return None, "requests error"
    
    flag = False
    description = ""
    
    # flag = False 删除失败，不需要重试：信息已不存在
    # flag = True 删除成功，不需要重试
    # flag = None 删除失败，需要重试：tg异常，tg限制
    
    if response is not None:
        response_text = json.loads(response.text)
        # print(response_text)
        print("kick: %s %s %s" % (chat_id, user_id, response_text))
        
        if "ok" in response_text:
            if response_text["ok"]:
                flag = True
            else:
                description = ""
                if "description" in response_text:
                    description = response_text["description"]
                
                if description in description_arr:
                    # 不用重试
                    flag = False
                
                if "error_code" in response_text:
                    error_code = str(response_text["error_code"])
                    
                    if error_code == "429":
                        if "parameters" in response_text and "retry_after" in response_text["parameters"]:
                            retry_after = int(response_text["parameters"]["retry_after"])
                            print("banChatMember sleep %s" % retry_after)
                            time.sleep(retry_after)
                            # 需要重试
                            flag = None
                    elif error_code == "403":
                        pass
        else:
            # tg异常重试
            flag = None
            description = "tg error"
    
    return flag, description
    
    
# ============================================================================================================================================
    
def getRestrictChatMemberRetry(result):
    flag = result[0]
    description = result[1]
    
    if flag is None:
        print("getRestrictChatMemberRetry: %s" % description)
        return True
    else:
        return False
        
        
def restrictChatMemberWrap(bot_url, user_id, until_date=-1):
    description = ""
    
    try:
        return restrictChatMember(bot_url, user_id, until_date)
    except Exception as e:
        description = e
        print("restrictChatMemberWrap Exception: %s" % e)
    
    return None, description
        
        
@retry(stop_max_attempt_number=3, retry_on_result=getRestrictChatMemberRetry)
def restrictChatMember(bot_url, user_id, until_date=-1):
    tg_url = bot_url + "restrictChatMember"
    
    headers = headers_tg
    
    data = {
        "chat_id": chat_id,
        "user_id": user_id,
        "until_date": until_date,
    }
    
    response = None
    try:
        response = requests.post(tg_url, json=data, headers=headers, timeout=15)
    except Exception as e:
        print("restrictChatMember Exception: %s" % e)
    
    if response is None:
        return None, "requests error"
    
    flag = False
    description = ""
    
    # flag = False 删除失败，不需要重试：信息已不存在
    # flag = True 删除成功，不需要重试
    # flag = None 删除失败，需要重试：tg异常，tg限制
    
    if response is not None:
        response_text = json.loads(response.text)
        # print(response_text)
        print("restrict: %s %s %s" % (chat_id, user_id, response_text))
        
        if "ok" in response_text:
            if response_text["ok"]:
                flag = True
            else:
                description = ""
                if "description" in response_text:
                    description = response_text["description"]
                
                if description in description_arr:
                    # 不用重试
                    flag = False
                
                if "error_code" in response_text:
                    error_code = str(response_text["error_code"])
                    
                    if error_code == "429":
                        if "parameters" in response_text and "retry_after" in response_text["parameters"]:
                            retry_after = int(response_text["parameters"]["retry_after"])
                            print("restrictChatMember sleep %s" % retry_after)
                            time.sleep(retry_after)
                            # 需要重试
                            flag = None
                    elif error_code == "403":
                        pass
        else:
            # tg异常重试
            flag = None
            description = "tg error"
    
    return flag, description


def setChatPhotoRequestRetry(result):
    flag = result[0]
    description = result[1]

    if flag is None:
        print("setChatPhotoRequestRetry: %s" % description)
        return True
    else:
        return False


@retry(stop_max_attempt_number=3, retry_on_result=setChatPhotoRequestRetry)
def setChatPhotoRequest(bot_url, chat_id, photo):
    tg_url = bot_url + "setChatPhoto"

    data = {
        "chat_id": chat_id,
    }

    response = None
    try:
        response = requests.post(tg_url, data=data, files={"photo": open(photo, 'rb')}, timeout=15)
    except Exception as e:
        print("setChatPhotoRequest Exception: %s" % e)

    if response is None:
        return None, "requests error"

    flag = False
    description = ""

    # flag = False 失败，不需要重试
    # flag = True 成功，不需要重试
    # flag = None 失败，需要重试：tg异常，tg限制

    if response is not None:
        print(response.text)
        response_text = json.loads(response.text)
        # print(response_text)
        print("setChatPhotoRequest %s %s %s" % (chat_id, photo, response_text))

        if "ok" in response_text:
            if response_text["ok"]:
                flag = True
            else:
                description = ""
                if "description" in response_text:
                    description = response_text["description"]

                if description in description_arr:
                    # 不用重试
                    flag = False

                if "error_code" in response_text:
                    error_code = str(response_text["error_code"])

                    if error_code == "429":
                        if "parameters" in response_text and "retry_after" in response_text["parameters"]:
                            retry_after = int(response_text["parameters"]["retry_after"])
                            print("setChatPhotoRequest sleep %s" % retry_after)
                            time.sleep(retry_after)
                            # 需要重试
                            flag = None
                    elif error_code == "403":
                        pass
        else:
            # tg异常重试
            flag = None
            description = "tg error"

    return flag, description
