import navigation
import energy
import laser

if __name__ == "__main__":
    try:
        # Platin Mountain coords: 49989, 76828
        energy.set_limit_normal()
        navigation.travel_position_until_recive(49989, 77000)

        energy.mine()
        laser.aim_laser()
    except KeyboardInterrupt:
        laser.deactive()
