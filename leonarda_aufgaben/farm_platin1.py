import navigation
import energy
import laser

if __name__ == "__main__":
    try:
        navigation.travel_position(49989, 76728)
        laser.aim_laser()

    except KeyboardInterrupt:
        laser.deactive()