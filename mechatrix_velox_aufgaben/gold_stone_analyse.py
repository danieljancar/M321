import navigation as nav
import energy

energy.set_limit_normal()
nav.travel_position_until_recive(-10000, 20500)

# der analyzer beta braucht viel energie -> reactor starten und braucht uran
energy.set_limits({
    "analyzer_beta": 1,
    "nuclear_reactor": 1,
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
