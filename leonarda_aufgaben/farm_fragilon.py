import navigation
import energy
import laser
import time

energy.set_limit_normal()
navigation.travel_position_until_recive(-53750, -44627)

energy.mine()
laser.aim_laser()

"""
laser.set_angle(110)

while True:
    laser.activate()
    time.sleep(7)
"""
