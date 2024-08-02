import db
import math

group_tg_id = "-1001872089701"
user_tg_id = "6668564628"

msg_tg_ids = db.msg48_get(group_tg_id, user_tg_id)

msg_tg_ids_len = len(msg_tg_ids)

print(msg_tg_ids_len)

if msg_tg_ids_len > 0:
    temp = 1
    temp_max = math.ceil(msg_tg_ids_len / 100)
    
    while temp <= temp_max:
        start = (temp - 1) * 100
        end = start + 100
        
        msg_tg_ids100 = msg_tg_ids[start:end]
            
        temp = temp + 1
        
        print(msg_tg_ids100)
        print(len(msg_tg_ids100))