from os import environ
import logging
import requests
import json

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

balances = {}

def hex2str(hex):
   """
   Decodes a hex string into a regular string
   """
   return bytes.fromhex(hex[2:]).decode("utf-8")

def str2hex(str):
   """
   Encodes a string as a hex string
   """
   return "0x" + str.encode("utf-8").hex()

def handle_update(data):
    input = hex2str(data['payload'])
    json_data = json.loads(input)
    account_rider = json_data['address_account_rider']
    account_driver = json_data['address_account_driver']
    price = json_data['price']
    if account_rider not in balances.keys():
        balances[account_rider] = 1000
    if account_driver not in balances.keys():
        balances[account_driver] = 1000

    if balances[account_rider] > price:
        balances[account_rider] -= price
        balances[account_driver] += price
    else:
        response = requests.post(rollup_server + "/report", json={"payload": str2hex('Error, you not have enough balance')})
        logger.info(f"Received report status {response.status_code} body {response.content}")

def handle_advance(data):

    input = hex2str(data['payload'])
    logger.info(f"Received advance request data {input}")
    
    json_data = json.loads(input)
    action = json_data["action"]

    if action == "Transfer":
        handle_update(data)

    return "accept"

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    
    print(data)
    input = hex2str(data['payload'])
    print(input)
    json_data = json.loads(input)
    print(json_data)
    action = json_data["action"]

    # Aqui verificamos se o payload corresponde ao caminho /balances
    if action == "Balance":
        balances_str = json.dumps(balances)
        response = requests.post(rollup_server + "/report", json={"payload": str2hex(balances_str)})
        logger.info(f"Received report status {response.status_code} body {response.content}")

    return str2hex("Invalid request")

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
