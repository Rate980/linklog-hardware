import pyaudio
from gpio import ConnectSense


class Stream:
    def __init__(
        self,
        conecct_sense: ConnectSense,
        chunk_size=1024,
        sample_rate=44100,
        input_=True,
        output=True,
    ):
        self.chunk_size = chunk_size
        self.sample_rate = sample_rate
        self.input = input_
        self.output = output
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=self.input,
            output=self.output,
            frames_per_buffer=self.chunk_size,
            stream_callback=self.callback,
        )

    def callback(self, in_data, frame_count, time_info, status):
        return None, pyaudio.paContinue

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
