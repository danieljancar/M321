import navigation
import energy
import json
import threading
import scanner

unique_stations = []

def wait_for_station():
    while True:
        for station in scanner.scan():
            if station not in unique_stations:
                f = open("stations.json", "a")
                f.write(json.dumps(station) + "\n")
                f.close()
                unique_stations.append(station)
                print(station)

def search_colony():
    center_x = 0
    center_y = 0

    deviation = 150000

    start_x = center_x - deviation
    end_x = center_x + deviation
    start_y = center_y - deviation
    end_y = center_y + deviation

    step_size = 3000

    x = start_x
    while x <= end_x:
        navigation.travel_position_until_recive(x, start_y)
        navigation.travel_position_until_recive(x, end_y)

        x += step_size

        if x <= end_x:
            navigation.travel_position_until_recive(x, end_y)
            navigation.travel_position_until_recive(x, start_y)


energy.set_limit_normal()
navigation.travel_position_until_recive(-80000, -80000)
thread_station = threading.Thread(target=wait_for_station)
thread_station.start()
search_colony()
thread_station.join()

# im stations.json nach station suchen für cords --> nav.travel_position_until_recive(-108503, -108888)