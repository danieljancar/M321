import requests

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
