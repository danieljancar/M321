import requests
import json

def get_status_node1():
    response = requests.get('http://10.255.255.254:2032/status')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get status. Status code: {response.status_code}")
        return None


def get_status_node2():
    response = requests.get('http://10.255.255.254:2033/status')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get status. Status code: {response.status_code}")
        return None


def get_active_node_url():
    status_node1 = get_status_node1()
    status_node2 = get_status_node2()

    if status_node1 and status_node1['role'] == 'active':
        return 'http://10.255.255.254:2032'
    elif status_node2 and status_node2['role'] == 'active':
        return 'http://10.255.255.254:2033'
    else:
        print("No active node found.")
        return None


def get_limits():
    response = requests.get('http://10.255.255.254:2032/limits')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get limits. Status code: {response.status_code}")
        return None


def set_limits(new_limits):
    headers = {'Content-Type': 'application/json'}
    url = get_active_node_url()

    response = requests.put(f"{url}/limits", data=json.dumps(new_limits), headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to set limits. Status code: {response.status_code}")
        return None


def set_limit_normal():
    set_limits({
        "thruster_back": 1,
        "thruster_front": 1,
        "thruster_bottom_left": 1,
        "thruster_front_right": 1,
        "thruster_bottom_right": 1,
        "thruster_front_left": 1,
        "scanner": 0,
        "laser": 0,
        "sensor_atomic_field": 1,
        "matter_stabilizer": 1
    })


def mine():
    set_limits({
        "scanner": 0,
        "thruster_back": 0.2,
        "thruster_front": 0.2,
        "thruster_bottom_left": 0.2,
        "thruster_front_right": 0.2,
        "thruster_bottom_right": 0.2,
        "thruster_front_left": 0.2,
        "laser": 1,
        "sensor_atomic_field": 0.2,
        "matter_stabilizer": 0.2
    })
