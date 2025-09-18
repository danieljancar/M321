import navigation as nav
import energy as e
import analyzer_gamma.analyzer_gamma as analyzer

nav.travel_position_until_recive(-95375, -90773)
e.set_limits({
    "sensor_antimatter": 1,
    "analyzer_gamma": 1,
    "analyzer_beta": 0,
    "analyzer_alpha": 0,
    "nuclear_reactor": 0,
    "jumpdrive": 0,
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

analyzer.run()