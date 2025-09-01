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

def move_first_row(vertical_size: int):
    response = requests.get("http://10.255.255.254:2012/structure")

    data = response.json().get("hold")
    row = data[0]

    for x_position, item in enumerate(row):
        if item is not None:
            items_in_column = find_items_in_column(data, x_position, vertical_size)
            if items_in_column == 0:
                continue
            move_item_down(x_position, items_in_column)
            break


def move_item_down(x_position, items_in_column):
    y_position = 0

    for y in range(items_in_column):
        out_data = {
            "a": {"x": x_position, "y": y_position},
            "b": {"x": x_position, "y": y_position + 1}
        }
        y_position += 1
        requests.post("http://10.255.255.254:2012/swap_adjacent", json=out_data).json()
        time.sleep(.5)


def find_items_in_column(data, column_index, vertical_size) -> int:
    items_in_column = vertical_size

    for row_index, row in reversed(list(enumerate(data))):
        item = row[column_index]

        if item is not None and items_in_column != 0:
            items_in_column -= 1
        else:
            break

    return items_in_column
