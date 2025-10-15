import navigation
import energy
import laser
import cargo_hold as cargo
import time

"""
navigation.travel_position_until_recive(-44450, 45728)

laser.aim_laser()
"""

energy.set_energy_mine(1, 0)
laser.set_angle(50)

while True:
    if cargo.must_move_item():
        cargo.move_all_down(.5)

    laser.activate()
    time.sleep(7)
