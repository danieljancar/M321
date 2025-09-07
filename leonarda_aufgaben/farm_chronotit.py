import navigation
import energy
import laser

energy.set_limit_normal()
navigation.travel_position_until_recive(-44450, 45728)

energy.mine()
laser.aim_laser()