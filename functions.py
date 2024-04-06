import json

# AFK related functions

afk_dict = {}

def CheckAfk(user_id: int):
    return user_id in afk_dict

def SaveAfk(user_id: int, status: str, timestamp: int):
    data = {str(user_id): {"status": status, "timestamp": timestamp}}
    afk_dict[user_id] = data
    return True

def RemoveAfk(user_id: int):
    afk_dict.pop(user_id)

def GetAfkStatus(user_id: int):
    return afk_dict[user_id]["status"]

def GetAfkTimestamp(user_id: int):
    return afk_dict[user_id]["timestamp"]
