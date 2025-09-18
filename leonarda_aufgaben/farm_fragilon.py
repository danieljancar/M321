import navigation
import energy
import laser
import time
import cargo_hold as cargo

energy.set_limit_normal()
navigation.travel_position_until_recive(-53750, -44627)

energy.mine()
laser.aim_laser()

"""
wenn man 20 fragilon hat mit jumpdrive zu core station

mehrmals springen weil core station zu weit weg ist --> siehe jumpdrive.py
"""

"""
laser.set_angle(264)

while True:
    if cargo.must_move_item():
        cargo.move_all_down(.5)

    laser.activate()
    time.sleep(7)
"""