import navigation as nav
import energy
import cargo_hold as cargo

"""
energy.set_limits({
    "thruster_back": 0.2,
    "thruster_front": 0.2,
    "thruster_bottom_left": 0.2,
    "thruster_front_right": 0.2,
    "thruster_bottom_right": 0.2,
    "thruster_front_left": 0.2,
    "scanner": 0,
    "laser": 0,
    "sensor_atomic_field": 1,
    "matter_stabilizer": 1,
    "laser_amplifier": 0,
    "sensor_plasma_radiation": 0,
    "cargo_bot": 0,
    "jumpdrive": 0
})
"""

energy.set_limit_normal()

"""
energy.set_limits({
    "nuclear_reactor": 1,
    "jumpdrive": 1,
    "scanner": 0,
    "laser": 0,
    "cargo_bot": 0,
    "thruster_back": 0,
    "thruster_front": 0,
    "thruster_bottom_left": 0,
    "thruster_front_right": 0,
    "thruster_bottom_right": 0,
    "thruster_front_left": 0,
})
"""

# architect colony - uran kaufen
# nav.travel_position_until_recive(-108503, -108888)


# cargo.move_all_down(.5)
