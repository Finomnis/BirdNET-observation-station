import logging

from .observation_station import ObservationStation

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

    with ObservationStation() as observation_station:
        observation_station.run()

if __name__ == "__main__":
    main()
