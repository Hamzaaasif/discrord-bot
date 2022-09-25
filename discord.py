import requests
import json
import time


def sendMessageToChannel(channelId,content, auth_token):
    print(f"Sending message to discord channel ==> {channelId}")
    req_url = f'https://discord.com/api/v9/channels/{channelId}/messages'
    payload = {
        'content': content
    }
    header = {
        'authorization': auth_token
    }
    r = requests.post(req_url, data=payload, headers=header)
    
    if(r.status_code == 200):
        print("Mesasge send successfully ... ")
        return r.status_code
    print("Error occured, not able to send message")
    
def login(email, password):
    print("Login to discord account .. ")
    login_url = 'https://discord.com/api/v9/auth/login'
    payload = {
        'captcha_key': None,
        'gift_code_sku_id': None,
        'login': email,
        'password': password,
        'login_source': None,
        'undelete': False        
    }
    r = requests.post(login_url, json=payload)
    if(r.status_code == 200):
        print("Login successful")
        res = r.json()
        return res['token']
    
    
    
def start():
    json_file= open('keys.json')
    input_data = json.load(json_file)
    
    email= input_data["discord_keys"]["email"]
    password = input_data["discord_keys"]["password"]
    
    channel_ids = ["1022271980029890570","1023221907031597088"]
    res_status = 200
    
    discord_data = {
        'content': 'This testing  for login failure',
        'token': input_data["discord_keys"]["auth_token"]
    }
    
    if(res_status is not 200):
        discord_data['token'] = login(email, password)
        
    for channelId in channel_ids:
        print(f"Posting message to channel ==> {channelId}")
        res_status = sendMessageToChannel(channelId,discord_data['content'],discord_data['token'])
        if(res_status is not 200):
            print("login Failed.")
            discord_data['token'] = login(email, password)
            res_status = sendMessageToChannel(channelId,discord_data['content'],discord_data['token'])
        print("Waiting 5 secs ...")
        time.sleep(5)
    
    print("All messages send successfully ... ")
    
    
start()






