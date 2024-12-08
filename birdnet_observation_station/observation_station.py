import pyaudio

import logging

log = logging.getLogger(__name__)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

class ObservationStation:

    def __init__(self):
        pass

    def __enter__(self) -> "ObservationStation":
        log.info("Open audio stream")
        self.pyaudio = pyaudio.PyAudio()
        self.stream = self.pyaudio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)
        return self
    def __exit__(self, type, value, traceback):
        log.info("Close audio stream")
        self.stream.close()
        self.pyaudio.terminate()

    def run(self):
        log.info(self.stream.get_time())
