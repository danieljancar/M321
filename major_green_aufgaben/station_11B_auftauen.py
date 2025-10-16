import navigation
import laser
import time

navigation.travel_position_until_recive(18910, 5536)

while True:
    laser.activate()
    time.sleep(7)
