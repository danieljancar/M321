import requests
import time

url = "http://10.255.255.254:2012/hold"

def get_free_hold():
    return get_cargo_hold()["hold"]["hold_free"]

def display_cargo_hold():
    data = get_cargo_hold()
    if "error" in data:
        print(data["error"])
    else:
        print("Status des Cargo Holds:")
        print(f"Credits: {data['hold']['credits']}")
        print(f"Gesamtkapazität: {data['hold']['hold_size']}")
        print(f"Freie Kapazität: {data['hold']['hold_free']}")
        print("Ressourcen im Lager:")
        for resource, amount in data["hold"]["resources"].items():
            print(f" - {resource}: {amount}")

def get_cargo_hold():
    return requests.get(url).json()

def get_structure():
    return requests.get("http://10.255.255.254:2012/structure")


def move_structure(payload):
    return requests.post("http://10.255.255.254:2012/swap_adjacent", json=payload)


def move_down_when_full(sleep=.5):
    has_to_be_moved = must_move_item()
    print("bewege nach unten wenn voll: " + str(has_to_be_moved))
    if has_to_be_moved:
        move_all_down(sleep)


def must_move_item():
    return all(item is not None for item in get_structure().json()["hold"][0])


def move_all_down(sleep):
    for y in range(get_last_none_row()):
        for x in range(12):
            print(move_structure({
                "a": {
                    "x": x,
                    "y": y
                },
                "b": {
                    "x": x,
                    "y": y + 1
                }
            }).json())
            time.sleep(sleep)

def get_last_none_row():
    last_none_row = 0
    for i, row in enumerate(get_structure().json()["hold"]):
        if any(cell is None for cell in row):
            last_none_row = i
    return last_none_row
