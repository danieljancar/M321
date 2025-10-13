import navigation
import energy
import laser

if __name__ == "__main__":
    try:
        navigation.travel_position(49989, 76600)
        laser.aim_laser()
        laser.activate()

    except KeyboardInterrupt:
        laser.deactive()