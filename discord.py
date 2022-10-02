import requests
import json
from loguru import logger

def sendMessageToChannel(channelId,content, auth_token):
    logger.debug(f"Sending message to discord channel: {channelId}")
    req_url = f'https://discord.com/api/v9/channels/{channelId}/messages'
    payload = {
        'content': content
    }
    header = {
        'authorization': auth_token
    }
    r = requests.post(req_url, data=payload, headers=header)
    
    if(r.status_code == 200):
        logger.info(f"Mesasge send successfully to channelId ===> {channelId} ")
        return r.status_code
    logger.error(f"Error occured, not able to send message : {r.json()}")
    return 400
    
def login(email, password):
    logger.debug(f"Try to login with email: {email}")
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
        logger.debug("Login success to discord")
        res = r.json()
        return res['token']
    error = r.json()
    logger.error(f"Failed to login to discord: error ==> {error}")
    return 400
    
    
    
def start(channelId, channel_msg):
    logger.info("Script start for sending discord messages")
    json_file= open('keys.json')
    input_data = json.load(json_file)
    
    email= input_data["discord_keys"]["email"]
    password = input_data["discord_keys"]["password"]
    res_status = 200
    
    discord_data = {
        'content': channel_msg,
        'token': input_data["discord_keys"]["auth_token"]
    }
    
    if(res_status != 200):
        discord_data['token'] = login(email, password)
        
    res_status = sendMessageToChannel(channelId,discord_data['content'],discord_data['token'])
    if(res_status != 200):
        logger.error("login Failed.")
        discord_data['token'] = login(email, password)
        logger.info("Attempting to send message again ..")
        res_status = sendMessageToChannel(channelId,discord_data['content'],discord_data['token'])
    return res_status







