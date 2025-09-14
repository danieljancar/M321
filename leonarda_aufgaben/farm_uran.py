import navigation
import energy
import laser
import cargo_hold as cargo
import time

"""
energy.set_limit_normal()
navigation.travel_position_until_recive(-21500, 36300)

energy.mine()
laser.aim_laser()
"""
# brüücht laser amplifier -> baut au stein ab
energy.mine()
laser.set_angle(168)

while True:
    if cargo.must_move_item():
        cargo.move_all_down(.5)

    laser.activate()
    time.sleep(7)
