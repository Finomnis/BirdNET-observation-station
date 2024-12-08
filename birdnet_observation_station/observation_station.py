import pyaudio

import numpy as np

from birdnetlib.main import RecordingBase
from birdnetlib.analyzer import Analyzer

import logging
log = logging.getLogger(__name__)


class RecordingStream(RecordingBase):
    def __init__(
        self,
        analyzer,
        rate,
        chunk_duration,
        week_48=-1,
        date=None,
        sensitivity=1.0,
        lat=None,
        lon=None,
        min_conf=0.1,
        overlap=0.0,
        return_all_detections=False,
    ):
        self.rate = rate
        self.chunk_duration = chunk_duration
        self.pyaudio = pyaudio.PyAudio()
        self.stream = self.pyaudio.open(format=pyaudio.paInt16, channels=1, rate=self.rate, input=True)
        super().__init__(
            analyzer,
            week_48,
            date,
            sensitivity,
            lat,
            lon,
            min_conf,
            overlap,
            return_all_detections,
        )

    @property
    def filename(self):
        return "buffer"

    def read_audio_data(self):
        stream_data = self.stream.read(int(self.chunk_duration * self.rate))
        #print(f"Leftover: {self.stream.get_read_available()}")
        #print(len(stream_data), type(stream_data))
        buffer = np.frombuffer(stream_data, dtype=np.int16)
        self.ndarray = buffer
        self.duration = len(self.ndarray) / self.rate
        #print(self.duration, buffer[:10])
        self.process_audio_data(self.rate)

    def close(self):
        self.stream.close()
        self.pyaudio.terminate()


class ObservationStation:

    def __init__(self):
        pass

    def __enter__(self) -> "ObservationStation":
        log.info("Open audio stream")
        self.analyzer = Analyzer()
        self.stream = RecordingStream(self.analyzer, rate=48000, chunk_duration=3.0, min_conf=0.2)
        return self
    def __exit__(self, type, value, traceback):
        log.info("Close audio stream")
        self.stream.close()

    def run(self):

        while True:
            self.stream.analyze()
            for detection in self.stream.detections:
                print(f"  - {detection['confidence']} {detection['common_name']}")
