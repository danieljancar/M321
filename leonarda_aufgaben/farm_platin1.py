import navigation
import energy
import laser
import requests

if __name__ == "__main__":
    try:
        navigation.travel_position(49989, 76782)
        laser.aim_laser()

        response = requests.get("http://10.255.255.254:2018/state")
        print(f"state: {response.json()}")

    except KeyboardInterrupt:
        laser.deactive()