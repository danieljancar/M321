import navigation
import laser
import time

navigation.travel_position_until_recive(8760, -9308)

while True:
    laser.activate()
    time.sleep(6)
