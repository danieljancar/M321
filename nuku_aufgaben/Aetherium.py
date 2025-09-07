import navigation
import energy
import laser


energy.set_limit_normal()
navigation.travel_position_until_recive(-95550, -90773)

energy.set_energy_mine(0, 1)
laser.aim_laser()

"""
laser.set_angle(234)
while True:
    laser.activate()
    time.sleep(7)
"""