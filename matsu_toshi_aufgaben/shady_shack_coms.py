import navigation
import energy
import time
import scanner
import json


def follow_captain_morris():
    while True:
        scan_result = scanner.scan()

        for ship in scan_result:
            if ship.get("name") == "Shady Shack":
                f = open("shady_shack_cords.json", "a")
                f.write(json.dumps(ship) + "\n")
                f.close()

            if ship.get("name") == "Captain Morris":
                pos = ship.get("pos")
                x, y = pos.get("x"), pos.get("y")

                print(f"Captain Morris: {x},{y}")
                navigation.travel_position(x, y)

                time.sleep(0.5)
                break
        time.sleep(0.5)

if __name__ == "__main__":
    energy.set_limit_normal()
    navigation.travel_position_until_recive(-11000, -11000)
    follow_captain_morris()
