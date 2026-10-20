from math import floor
import time
import numpy as np
import sounddevice as sd
import tkinter as tk
from collections import deque
import queue

from notes.leastsquare import Amat, NOTES, get_notes
from notes.interface import Interface

class Audio:
# Audio configuration
    FS = 44100
    WINDOW_SECONDS = 0.1
    WINDOW_SIZE = int(FS * WINDOW_SECONDS)
    BLOCK_SIZE = 1024
    UPDATE_SECONDS = 0.05


    def __init__(self):
# A rolling buffer containing the latest audio samples
        self.audio_buffer = deque(maxlen=Audio.WINDOW_SIZE)
        self.results_queue = queue.Queue()

# Precompute the least-squares matrix for the fixed
# time positions and candidate frequencies.
        t = np.arange(Audio.WINDOW_SIZE) / Audio.FS
        self.A_pinv = Amat(t)

        self.last_update = 0.0


    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(status)

        # Mono microphone input
        self.audio_buffer.extend(indata[:, 0].copy())


    def analyse(self):

        now = time.monotonic()
        if now - self.last_update < Audio.UPDATE_SECONDS:
            return
        self.last_update = now

        if len(self.audio_buffer) < Audio.WINDOW_SIZE:
            return

        samples = np.asarray(self.audio_buffer)

        amplitudes = get_notes(self.A_pinv, samples)

        self.results_queue.put(amplitudes)

    def get(self):
        return sd.InputStream(
            samplerate=Audio.FS,
            channels=1,
            dtype="float32",
            blocksize=Audio.BLOCK_SIZE,
            callback=self.audio_callback
            )


if __name__ == "__main__":
    audio = Audio()
    with audio.get():
        interface = Interface(audio)

        audio.analyse()
        interface.update_interface()
        interface.root.mainloop()
