import tkinter as tk
import queue
import numpy as np

from .leastsquare import NOTES

FONT_NAME = "Noto Serif"
class Interface:
    def __init__(self, audio):
        self.audio = audio
        self.root = tk.Tk()
        self.root.title("Note Detector")
        self.root.geometry("500x450")
        self.root.configure(bg="white")

# Main detected note
        self.main_note = tk.Label(
            self.root,
            text="Listening...",
            font=(FONT_NAME, 512, "bold"),
            fg="black",
            bg="white"
        )
        self.main_note.pack(pady=(20, 0), expand=False)

        self.main_amplitude = tk.Label(
            self.root,
            text="",
            font=(FONT_NAME, 16),
            fg="black",
            bg="white"
        )
        self.main_amplitude.pack(pady=(0, 25))

# Other detected notes
        self.other_notes = tk.Label(
            self.root,
            text="",
            font=(FONT_NAME, 17),
            fg="#4f4f4f",
            bg="white",
            justify="center"
        )
        self.other_notes.pack(pady=10)


    def update_interface(self):
        # Display the newest analysis result, if available
        latest = None

        try:
            while True:
                latest = self.audio.results_queue.get_nowait()
        except queue.Empty:
            pass

        if latest is not None:
            amplitudes = latest
            order = np.argsort(amplitudes)[::-1]

            strongest = order[0]

            self.main_note.config(text=NOTES[strongest])
            self.main_amplitude.config(
                text=f"Amplitude: {amplitudes[strongest]:.3f}"
            )

            others = [
                f"{NOTES[i]:<4}  {amplitudes[i]:.3f}"
                for i in order[1:6]
            ]
            self.other_notes.config(text="\n".join(others))

        self.audio.analyse()
        self.root.after(10, self.update_interface)
