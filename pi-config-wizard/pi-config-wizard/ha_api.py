
import os

base_url="http://supervisor/"
token = None
headers = None

def is_homeassistant_addon():
    return 'SUPERVISOR_TOKEN' in os.environ

def init():
    global headers, token
    if token is not None and headers is not None:
        return
    if is_homeassistant_addon():
        token = os.environ['SUPERVISOR_TOKEN']
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

def get(endpoint):
    init()
    import requests
    url = f"{base_url}{endpoint}"
    r = requests.get(url, headers=headers)
    return r.json()

def set(endpoint, data=None):
    init()
    import requests
    url = f"{base_url}{endpoint}"
    requests.post(url, headers=headers)

def get_ips():
    ips = {}
    data = get("network/info")
    interfaces = data["data"]["interfaces"]
    for interface in interfaces:
        name = interface['interface']
        ip = interface['ipv4']['address']
        if len(ip) == 0:
            continue
        ip = ip[0]
        if ip == '':
            continue
        if "/" in ip:
            ip = ip.split("/")[0]
        ips[name] = ip
    return ips

def get_network_connection_type():
    connection_type_map = {
        "ethernet": "Wired",
        "wireless": "Wireless",
    }
    connection_type = []
    data = get("network/info")
    interfaces = data["data"]["interfaces"]
    for interface in interfaces:
        if interface['connected']:
            connection_type.append(connection_type_map[interface['type']])
    return connection_type

def shutdown():
    '''shutdown homeassistant host'''
    set("host/shutdown")

def reboot():
    '''reboot homeassistant host'''
    set("host/reboot")
