import navigation
import energy
import laser

# TODO: braucht massenstabilisator sonst verfällt das chronotit zu nuklearem abfall
navigation.travel_position_until_recive(-44850, 45728)
energy.mine()
laser.aim_laser()