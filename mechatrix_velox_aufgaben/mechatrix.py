import navigation
import energy

"""
1. uran haben für reactor
2. so weit wie möglich zu 150000/150000 fliegen
3. dann nur jumpdrive und reactor energie geben und dann mit jumpdrive zu diesen koordinaten
"""

energy.set_limit_normal()
navigation.travel_position_until_recive(142000, 142000)
energy.set_limits({
    "nuclear_reactor": 1,
    "jumpdrive": 1,
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
# jumpdrive ausführen wenn 100% aufgeladen sind