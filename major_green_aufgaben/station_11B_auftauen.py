import navigation
import laser
import time

navigation.travel_position_until_recive(18910, 5456)

while True:
    laser.aim_laser()
    time.sleep(7)
