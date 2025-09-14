import navigation as nav
import energy
import cargo_hold as cargo

"""
energy.set_limits({
    "thruster_back": 1,
    "thruster_front": 1,
    "thruster_bottom_left": 1,
    "thruster_front_right": 1,
    "thruster_bottom_right": 1,
    "thruster_front_left": 1,
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

# energy.set_limit_normal()

energy.set_limits({
    "nuclear_reactor": 0,
    "jumpdrive": 0,
    "scanner": 0,
    "laser": 0,
    "sensor_atomic_field": 0,
    "matter_stabilizer": 0,
    "cargo_bot": 1,
    "thruster_back": 1,
    "thruster_front": 1,
    "thruster_bottom_left": 1,
    "thruster_front_right": 1,
    "thruster_bottom_right": 1,
    "thruster_front_left": 1,
})

# nav.travel_position_until_recive(150000, 150000)


"""
energy.set_limits({
    "nuclear_reactor": 0,
    "jumpdrive": 0,
    "scanner": 0,
    "laser": 0,
    "cargo_bot": 1,
    "sensor_atomic_field": 1,
    "matter_stabilizer": 1,
    "thruster_back": 1,
    "thruster_front": 1,
    "thruster_bottom_left": 1,
    "thruster_front_right": 1,
    "thruster_bottom_right": 1,
    "thruster_front_left": 1
})
"""

# architect colony - uran kaufen
# nav.travel_position_until_recive(-108503, -108888)


# cargo.move_all_down(.5)
