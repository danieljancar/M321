import navigation
import energy
import laser
import cargo_hold as cargo
import time

navigation.travel_position_until_recive(49989, 76828)

energy.mine()
laser.activate()
time.sleep(5)
cargo.display_cargo_hold()
laser.deactive()
