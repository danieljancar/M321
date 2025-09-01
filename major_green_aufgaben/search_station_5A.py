import scanner
import energy
import navigation
import time

energy.set_limit_normal()

def follow_station(target_name):
    while True:
        scan_result = scanner.scan()
        if not scan_result:
            time.sleep(1)
            continue

        for obj in scan_result:
            if obj.get("name") == target_name:
                pos = obj.get("pos", {})
                x, y = pos.get("x"), pos.get("y")
                if x is None or y is None:
                    continue

                print(f"Ziel: {target_name} bei x={x}, y={y}")
                navigation.travel_position_until_recive(x, y)
                print(f"{target_name} erreicht, weiter scannen ...")

                time.sleep(.5)
                break
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        navigation.travel_position_until_recive(15400, -11200)
        follow_station("Station 5-A")
    except KeyboardInterrupt:
        print("\nScript gestoppt")
