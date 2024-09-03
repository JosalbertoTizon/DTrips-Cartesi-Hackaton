import requests
import folium
import psycopg2
import json
from web3 import Web3
from inputBoxAbi import INPUTBOX_ABI
api_key = '5b3ce3597851110001cf6248a2174ddbf4e9447f9ece3763416a1719'

#FUNCTION TO REGISTER:

def sign_up (classification, name, password, account, email):
    try:
        connection = psycopg2.connect("postgres://default:L8Ose7rCDJRb@ep-tiny-art-a4fcdees-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
    except:
        print('Error in connection with database')
        return "connect"

    cursor = connection.cursor()
    
    if classification == 'Rider':
        
        try:
            cursor.execute('INSERT INTO records (classification, username, password, account, email) VALUES (%s, %s, %s, %s, %s)', (1, name, password, account, email))
            connection.commit()
            return "success"
        except:
            print("Error to register rider")
            return "register"
    
    elif classification == 'Driver':
        
        try:
            cursor.execute('INSERT INTO records (classification, username, password, account, email) VALUES (%s, %s, %s, %s, %s)', (2, name, password, account, email))
            connection.commit()
            print('Successful registration')
            return "success"
        except:
            print('Error to register driver')
            return "register"

#FUNCTION TO LOGIN

def login (name, password):
    try:
        connection = psycopg2.connect("postgres://default:L8Ose7rCDJRb@ep-tiny-art-a4fcdees-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
    except:
        print('Error in connection with database')
        return "connect", None

    cursor = connection.cursor()

    cursor.execute('SELECT * FROM records WHERE username = %s', (name,))
    result = cursor.fetchone()

    if result is None:
        print('User inst registered\n')
        return "register", None
    else:
        if password == result[3] and result[1] == 1:
            print('Login success!')
            return "success", "Rider"
        elif password == result[3] and result[1] == 2:
            print('Login success!')
            return "success", "Driver"

#FUNCTION TO GET THE COORDINATES

def get_coordinates(address):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'json',
        'limit': 1
    }

    headers = {
        'User-Agent': 'Teste1/1.0 (leoaguiar727@gmail.com)'
    }
    
    response = requests.get(url, params = params, headers = headers)

    try:
        data = response.json()
    except ValueError:
        print("Erro ao decodificar JSON")
        return None, None
    
    if data:
        location = data[0]['lat'], data[0]['lon']
        return location
    else:
        print("Geocoding error: Address not found")
        return "Invalid"

#FUNCTION TO CALCULATE THE DISTANCE AND DURATION

def get_distance_and_duration(start_address, end_address, api_key):
    try:
        start_lat, start_lng = get_coordinates(start_address)
        end_lat, end_lng = get_coordinates(end_address)
    except:
        return "error", None, None

    url = 'https://api.openrouteservice.org/v2/directions/driving-car'
    
    params = {
        'api_key': api_key,
        'start': f'{start_lng},{start_lat}',
        'end': f'{end_lng},{end_lat}'
    }

    response = requests.get(url, params = params)
    
    try:
        data = response.json()
    except ValueError:
        print("Error decoding JSON")
        return None, None, None

    summary = data['features'][0]['properties']['summary']
    distance = summary['distance'] / 1000  # Distância em quilômetros
    duration = summary['duration'] / 60  # Duração em minutos

    coordinates = data['features'][0]['geometry']['coordinates']
    route_coords = [(coord[1], coord[0]) for coord in coordinates]

    return distance, duration, route_coords

def passenger_request (name, start_address, end_address):
    try:
        connection = psycopg2.connect("postgres://default:L8Ose7rCDJRb@ep-tiny-art-a4fcdees-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
    except:
        print('Error in connection with database')
        return "connect"

    cursor = connection.cursor()

    try:
        cursor.execute('INSERT INTO passengers (name, start_address, end_address) VALUES (%s, %s, %s)', (name, start_address, end_address))
        connection.commit()
        print('Request successful')
        return "success"
    except:
        print('Error in request')
        return "error"

def driver_location (name, start_address):
    try:
        connection = psycopg2.connect("postgres://default:L8Ose7rCDJRb@ep-tiny-art-a4fcdees-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
    except:
        print('Error in connection with database')
        return "error"

    cursor = connection.cursor()

    try:
        cursor.execute('INSERT INTO drivers (name, start_address) VALUES (%s, %s)', (name, start_address))
        connection.commit()
        print('Drivers location submitted')
        return "success"
    except:
        print('Error in driver location')
        return "error"

def price (distance, duration):

    rec_price = 0.5 + 0.22*distance + 0.09*duration

    return rec_price

def rides_for_driver (name):
    try:
        connection = psycopg2.connect("postgres://default:L8Ose7rCDJRb@ep-tiny-art-a4fcdees-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
    except:
        print('Error in connection with database')
        return None, "error"

    cursor = connection.cursor()

    cursor.execute('SELECT * FROM drivers WHERE name = %s', (name,))
    driver_data = cursor.fetchone()

    passengers_radio = []

    if driver_data is None:
        print('Driver isnt avaible')
    else:
        dr_address = driver_data[2]
        cursor.execute('SELECT * FROM passengers')
        passengers_data = cursor.fetchall()

        for passenger in passengers_data:
            passenger_name = passenger[1]
            pa_st_address = passenger[2]
            pa_en_address = passenger[3]
            
            distance, duration, _ = get_distance_and_duration(dr_address, pa_st_address, api_key)

            if distance <= 5:
                dicti = {'name': passenger_name, 'start_address': pa_st_address, 'end_address': pa_en_address, 'distance': distance, 'duration': duration}
                passengers_radio.append(dicti)

    if cursor:
        cursor.close()
    if connection:
        connection.close()

    return passengers_radio, "success"

def get_balance(username):
    try:
        connection = psycopg2.connect("postgres://default:L8Ose7rCDJRb@ep-tiny-art-a4fcdees-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
    except:
        print('Error in connection with database')
        return "error"
    
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM records WHERE username = %s', (username, ))
    result = cursor.fetchone()
    balance = int(result[4])
    return balance

def set_balance(username, amount):
    try:
        connection = psycopg2.connect("postgres://default:L8Ose7rCDJRb@ep-tiny-art-a4fcdees-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
    except:
        print('Error in connection with database')
        return "error"
    current_b = get_balance(username)
    cursor = connection.cursor()
    cursor.execute('UPDATE records SET account = %s WHERE username = %s', (current_b-amount, username))
    result = cursor.fetchone()
    balance = int(result[4])
    return balance

def update_status (rider_name):
    try:
        connection = psycopg2.connect("postgres://default:L8Ose7rCDJRb@ep-tiny-art-a4fcdees-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
    except:
        print('Error in connection with database')
        return "error"

    cursor = connection.cursor()   

    cursor.execute('SELECT * FROM rides WHERE rider_name = %s', (rider_name, ))
    result = cursor.fetchone()

    if result is None:
        print('Ride is not yet confirmed')
        return "unconfirmed"
    else:
        print('Ride is confirmed!')
        return "confirmed"
        
def rides_in_progress (rider_name, driver_name, start_address, end_address):
    try:
        connection = psycopg2.connect("postgres://default:L8Ose7rCDJRb@ep-tiny-art-a4fcdees-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
    except:
        print('Error in connection with database')
        return "error"

    cursor = connection.cursor()   

    try:
        cursor.execute('INSERT INTO rides (rider_name, driver_name, start_address, end_address) VALUES (%s, %s, %s, %s)', (rider_name, driver_name, start_address, end_address))
        connection.commit()
        print('Ride in progress')
        return "success"
    except:
        print('Error to confirm ride')
        return "error"
    
def delete_user (name_table, username):
    try:
        connection = psycopg2.connect("postgres://default:L8Ose7rCDJRb@ep-tiny-art-a4fcdees-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
    except:
        print('Error in connection with database')

    cursor = connection.cursor()       
    
    if name_table == 'passengers':
        cursor.execute('DELETE FROM passengers WHERE name = %s', (username,))
        connection.commit()
        print('User deleted from passengers')
    
    if name_table == 'drivers':
        cursor.execute('DELETE FROM drivers WHERE name = %s', (username,))
        connection.commit()
        print('User deleted from drivers')
    
    if name_table == 'rides':
        cursor.execute('DELETE FROM rides WHERE rider_name = %s', (username,))
        connection.commit()
        print('User deleted from rides')

def validation_address (address):
    location = get_coordinates(address)

    if location == 'Invalid':
        return "Invalid address"
    else:
        return "Valid address"
    
def send_information(account_rider, account_driver, price, key):
    data = {
        "address_account_rider": account_rider,
        "address_account_driver": account_driver,
        "price": price,
        "action": "Transfer"
    }

    account_rider = Web3.to_checksum_address(account_rider)
    account_driver = Web3.to_checksum_address(account_driver)
    contract_address = Web3.to_checksum_address('0x59b22D57D4f067708AB0c00552767405926dc768')
    dapp_address = Web3.to_checksum_address('0xab7528bb862fb57e8a2bcd567a2e929a0be56a5e')

    data_json = json.dumps(data)
    print(data_json)

    data_bytes = data_json.encode('utf-8')

    web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    contract = web3.eth.contract(address = contract_address, abi = INPUTBOX_ABI)

    tx = contract.functions.addInput(dapp_address, data_bytes).build_transaction({
    'from': account_rider,
    'nonce': web3.eth.get_transaction_count(account_rider),
    })

    signed_tx = web3.eth.account.sign_transaction(tx, key)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Transação enviada. Hash: {web3.to_hex(tx_hash)}")
    
def fetch():
    # URL da rota
    url = 'http://localhost:8080/inspect/%7B%20"action":%20"Balance"%20%7D'

    try:
        # Fazendo o GET request
        response = requests.get(url)
        
        # Verificando se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Manipulando o conteúdo da resposta
            data =response.json()  # Se a resposta for JSON
            print("Dados recebidos:")
            print(data)
            print(data['reports'][0]['payload'])
            return json.loads(hex2str(data['reports'][0]['payload']))
        else:
            print(f"Erro na requisição: {response.status_code}")
            print(response.text)
            return 'error'
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar à rota: {e}")
        return 'error1'

def hex2str(hex):
    """
    Decodes a hex string into a regular string
    """
    return bytes.fromhex(hex[2:]).decode("utf-8")

def get_account(username):
    try:
        connection = psycopg2.connect("postgres://default:L8Ose7rCDJRb@ep-tiny-art-a4fcdees-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
    except:
        print('Error in connection with database')
        return "connect"

    cursor = connection.cursor()

    cursor.execute('SELECT * FROM records WHERE username = %s', (username,))
    result = cursor.fetchone()

    return result[4]
    
def get_driver_name(rider_name):
    try:
        connection = psycopg2.connect("postgres://default:L8Ose7rCDJRb@ep-tiny-art-a4fcdees-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
    except:
        print('Error in connection with database')
        return "connect"

    cursor = connection.cursor()

    cursor.execute('SELECT * FROM rides WHERE rider_name = %s', (rider_name,))
    result = cursor.fetchone()

    return result[2]