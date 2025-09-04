import navigation
import energy
import laser

# TODO: cargo bot muss items nach unten räumen sonst kein platz
navigation.travel_position_until_recive(-44900, 45728)
energy.set_limits({
    "thruster_back": 0.2,
    "thruster_front": 0.2,
    "thruster_bottom_left": 0.2,
    "thruster_front_right": 0.2,
    "thruster_bottom_right": 0.2,
    "thruster_front_left": 0.2,
    "laser": 1,
    "scanner": 0,
    "sensor_void_energy": 0,
    "sensor_antimatter": 0,
    "sensor_atomic_field": 1,
    "matter_stabilizer": 1
})
laser.aim_laser()