import navigation as nav
import energy

energy.set_limit_normal()
nav.travel_position_until_recive(-51568, -52709)
energy.set_limits({
    "subspace_tachyon_scanner": 1,
    "sensor_newton_depth": 1,
    "analyzer_delta": 1,
    "scanner": 0,
    "laser": 0,
    "sensor_atomic_field": 0,
    "matter_stabilizer": 0,
    "cargo_bot": 0,
    "thruster_back": 0,
    "thruster_front": 0,
    "thruster_bottom_left": 0,
    "thruster_front_right": 0,
    "thruster_bottom_right": 0,
    "thruster_front_left": 0,
})
