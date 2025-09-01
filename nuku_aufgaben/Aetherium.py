import navigation
import energy
import laser
import time

energy.set_limit_normal()
navigation.travel_position_until_recive(-95500, -90773)

energy.mine()
while True:
    # funktioniert nicht bzw. kein aetherium wird abgebaut
    laser.set_angle(176)
    laser.activate()
    time.sleep(7)


