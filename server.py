import asyncio
import os
import sys
import httpx
import random
import uuid
import datetime
from time import time
from loguru import logger
from httpx_socks import AsyncProxyTransport

# Disable logging for httpx
httpx_log = logger.bind(name="httpx").level("WARNING")
logger.remove()
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
                                   " | <level>{level: <8}</level>"
                                   " | <cyan><b>{line}</b></cyan>"
                                   " - <white><b>{message}</b></white>")
logger = logger.opt(colors=True)

GAMES = {
    1: {
        'name': 'Chain Cube 2048',
        'appToken': 'd1690a07-3780-4068-810f-9b5bbf2931b2',
        'promoId': 'b4170868-cef0-424f-8eb9-be0622e8e8e3',
    },
    2: {
        'name': 'Train Miner',
        'appToken': '82647f43-3f87-402d-88dd-09a90025313f',
        'promoId': 'c4480ac7-e178-4973-8061-9ed5b2e17954',
    },   
    3: {
        'name': 'Merge Away',
        'appToken': '8d1cc2ad-e097-4b86-90ef-7a27e19fb833',
        'promoId': 'dc128d28-c45b-411c-98ff-ac7726fbaea4'
    },
    4: {
        'name': 'Twerk Race 3D',
        'appToken': '61308365-9d16-4040-8bb0-2f4a4c69074c',
        'promoId': '61308365-9d16-4040-8bb0-2f4a4c69074c'
    },
    5 : {
        'name' : 'Polysphere',
        'appToken' : '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71',
        'promoId' : '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71'
    },
    6 : {
        'name' : 'Mow and Trim',
        'appToken' : 'ef319a80-949a-492e-8ee0-424fb5fc20a6',
        'promoId' : 'ef319a80-949a-492e-8ee0-424fb5fc20a6'
    }, 
    7 : {
        'name': 'Zoopolis',
        'appToken': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b',
        'promoId': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b'
    },
    8 : {
        'name': 'Tile Trio',
        'appToken': 'e68b39d2-4880-4a31-b3aa-0393e7df10c7',
        'promoId': 'e68b39d2-4880-4a31-b3aa-0393e7df10c7'
    },  
    9 : {
        'name': 'Fluff Crusade',
        'appToken': '112887b0-a8af-4eb2-ac63-d82df78283d9',
        'promoId': '112887b0-a8af-4eb2-ac63-d82df78283d9'
    },
    10 : {
        'name': 'Stone Age',
        'appToken': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af',
        'promoId': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af'
    },
    11: {
        'name': 'Bouncemasters',
        'appToken': 'bc72d3b9-8e91-4884-9c33-f72482f0db37',
        'promoId': 'bc72d3b9-8e91-4884-9c33-f72482f0db37'
    },
    12: {
        'name': 'Hide Ball',
        'appToken': '4bf4966c-4d22-439b-8ff2-dc5ebca1a600',
        'promoId': '4bf4966c-4d22-439b-8ff2-dc5ebca1a600'
    },
    13: {
        'name': 'Pin Out Master',
        'appToken': 'd2378baf-d617-417a-9d99-d685824335f0',
        'promoId': 'd2378baf-d617-417a-9d99-d685824335f0'
    },
    14: {
        'name': 'Count Masters',
        'appToken': '4bdc17da-2601-449b-948e-f8c7bd376553',
        'promoId': '4bdc17da-2601-449b-948e-f8c7bd376553'
    },
    15: {
        'name': 'Infected Frontier',
        'appToken': 'eb518c4b-e448-4065-9d33-06f3039f0fcb',
        'promoId': 'eb518c4b-e448-4065-9d33-06f3039f0fcb'
    },
    16: {
        'name': 'Among Water',
        'appToken': 'daab8f83-8ea2-4ad0-8dd5-d33363129640',
        'promoId': 'daab8f83-8ea2-4ad0-8dd5-d33363129640'
    },
    17: {
        'name': 'Factory World',
        'appToken': 'd02fc404-8985-4305-87d8-32bd4e66bb16',
        'promoId': 'd02fc404-8985-4305-87d8-32bd4e66bb16'
    }

}

BASE_URL = 'https://api.gamepromo.io'
EVENTS_DELAY = 30
HTTPX_TIMEOUT = 45
PROXY_TIMEOUT = 20

async def get_proxies(client_id):
    async with httpx.AsyncClient() as client:
        logger.info(f"Fetching Proxies id: {client_id}")
        proxies_response = await client.get("https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=json&anonymity=Anonymous,Elite&timeout=20000", timeout=20)
        proxies_data = proxies_response.json()

        ACCEPTABLE_LAST_CHECKED_TIME = 600
        acceptable_proxies = []
        for proxy in proxies_data['proxies']:
            if (time() - proxy['last_seen']) <= ACCEPTABLE_LAST_CHECKED_TIME:
                acceptable_proxies.append(proxy["proxy"])

        return acceptable_proxies
            

async def is_proxy_valid(proxy, client_id):
    if proxy is not None:
        transport = AsyncProxyTransport.from_url(proxy, verify=False)
    else:
        transport = None

    async with httpx.AsyncClient(transport=transport) as client:
        try:
            logger.info(f"Checking proxy validity id: {client_id}")
            response = None
            response = await client.get(f"{BASE_URL}/promo/login-client", timeout=PROXY_TIMEOUT)
            logger.info(f"Response Status Code: {response.status_code}")
            if response.content == b'NOT_FOUND':
                logger.success(f"Proxy is valid id: {client_id}")
                logger.info(f"Valid Proxy {proxy}")
                logger.info(f"Valid response: {response.content}".replace("<","\\<").replace(">","\\>"))
                return True
            else:
                logger.warning(f"Proxy is invalid id:{client_id}")
                logger.info(f"Invalid Response: {response.content}".replace("<","\\<").replace(">","\\>"))
                return False
        except Exception as e:
            logger.error(f"Proxy is invalid: {e} id: {client_id}")
            logger.error(f"Invalid proxy: {proxy}")
            if response is not None:
                logger.info(f"Invalid Response: {response.content}")
            return False

async def pick_a_proxy(proxies, client_id):
    proxy = random.choice(proxies)
    valid_proxy = ""
    for _ in range(len(proxies)):
        is_valid = await is_proxy_valid(proxy, client_id)
        if not is_valid:
            proxy = random.choice(proxies)
        else:
            valid_proxy = proxy
            return valid_proxy

    if not valid_proxy:
        logger.critical("Unlucky! Absolutely no valid proxies. Try again in 5 minutes")
        return

async def login(client_id, app_token, proxy):
    headers = {
        "User-Agent": "UnityPlayer/2022.3.20f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "Connection": "close"
    }

    if proxy is not None:
        transport = AsyncProxyTransport.from_url(proxy, verify=False)
    else:
        transport = None

    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.post(
            f'{BASE_URL}/promo/login-client',
            headers=headers,
            json={'appToken': app_token, 'clientId': client_id, 'clientOrigin': 'android'},
            timeout=httpx.Timeout(HTTPX_TIMEOUT)  
        )
        response.raise_for_status()
        client_token = response.json()['clientToken']
        logger.info(f"Logged in with Client Token: {client_token}")

        return client_token

async def register_event(client_token, promo_id, proxy):
    headers = {
        "Authorization": f"Bearer {client_token}",
        "User-Agent": "UnityPlayer/2022.3.20f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "Connection": "close"
    }
    has_code = False

    if proxy is not None:
        transport = AsyncProxyTransport.from_url(proxy, verify=False)
    else:
        transport = None

    async with httpx.AsyncClient(transport=transport) as client:
        while True:
            delay_time = EVENTS_DELAY * (random.uniform(0,0.33) + 1)
            logger.info(f"Sleeping for {delay_time} seconds.")
            await asyncio.sleep(delay_time)

            logger.info(f"Sending register request... id: {client_token.split(':')[2]}")
            response = await client.post(
                f'{BASE_URL}/promo/register-event',
                headers=headers,
                json={'promoId': promo_id, 'eventId': str(uuid.uuid4()), 'eventOrigin': 'undefined'},
                timeout=HTTPX_TIMEOUT  
            )
            logger.info(f"Response received: {response.json()} id: {client_token.split(':')[2]}")

            if 'hasCode' in response.json():
                has_code = response.json()['hasCode']

                if has_code:
                    logger.info(f"Code is ready! id: {client_token.split(':')[2]}")
                    break
                
            logger.info(f"Code is not ready. id: {client_token.split(':')[2]}")

        return has_code


async def create_code(client_token, promo_id, proxy):
    headers = {
        "Authorization": f"Bearer {client_token}",
        "User-Agent": "UnityPlayer/2022.3.20f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "Connection": "close"
    }

    if proxy is not None:
        transport = AsyncProxyTransport.from_url(proxy, verify=False)
    else:
        transport = None

    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.post(
            f'{BASE_URL}/promo/create-code',
            headers=headers,
            json={'promoId': promo_id},
            timeout=httpx.Timeout(HTTPX_TIMEOUT)
        )
        response.raise_for_status()
        key = response.json()['promoCode']

        logger.success(f"Key Generated: {key} id: {client_token.split(':')[2]}")
        return key


async def play_the_game(app_token, promo_id, use_proxies):
    client_id = str(uuid.uuid4())
    while True:
        proxy = None
        if use_proxies:
            if os.stat("proxies.txt").st_size != 0:
                logger.info("Non-empty proxies.txt file found")
                with open(file_path, 'r') as file:
                    proxies = [line.strip() for line in file if line.strip()]
                    proxy = random.choice(proxies)
            else:
                proxies = await get_proxies(client_id)
                proxy = await pick_a_proxy(proxies, client_id)
                if proxy is None:
                    continue
            
        try:
            logger.info(f"Sending login request... id: {client_id}")
            client_token = await login(client_id, app_token, proxy)

        except Exception as e:
            logger.error(f"Failed to login: {e} id: {client_id}")
            continue

        try:
            has_code = await register_event(client_token, promo_id, proxy)

        except Exception as e:
            logger.error(f"Failed to register event: {e} id: {client_id}")
            continue

        try:
            logger.info(f"Sending create request... id: {client_id}")
            key = await create_code(client_token, promo_id, proxy)
            return key

        except Exception as e:
            logger.error(f"An error occured while trying to create the code: {str(e)} id: {client_id}")
            continue

async def run(chosen_game, no_of_keys, use_proxies):
    if no_of_keys == 1:
        logger.info(f"Generating {no_of_keys} key for {GAMES[chosen_game]['name']}")
    else:
        logger.info(f"Generating {no_of_keys} keys for {GAMES[chosen_game]['name']}")

    tasks = [play_the_game(GAMES[chosen_game]['appToken'], GAMES[chosen_game]['promoId'], use_proxies) for _ in range(no_of_keys)]
    for completed_task in asyncio.as_completed(tasks):
        key = await completed_task
        yield key

