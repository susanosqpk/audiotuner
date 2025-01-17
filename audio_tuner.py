import pyaudio
import numpy as np
import tkinter as tk
from tkinter import ttk

class AudioTuner:
    def __init__(self):
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 2
        self.fs = 44100

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.fs,
                                  input=True,
                                  frames_per_buffer=self.chunk)

    def get_audio_data(self):
        data = self.stream.read(self.chunk)
        return np.frombuffer(data, dtype=np.int16)

    def apply_gain(self, data, gain):
        factor = 10 ** (gain / 20)
        return data * factor

    def process_audio(self, gain):
        audio_data = self.get_audio_data()
        processed_data = self.apply_gain(audio_data, gain)
        return processed_data

    def start(self):
        self.root = tk.Tk()
        self.root.title("AudioTuner")

        self.gain_label = ttk.Label(self.root, text="Gain (dB):")
        self.gain_label.pack()
        
        self.gain_value = tk.DoubleVar(value=0.0)
        self.gain_slider = ttk.Scale(self.root, from_=-20, to=20, variable=self.gain_value, orient='horizontal')
        self.gain_slider.pack()

        self.update_button = ttk.Button(self.root, text="Update", command=self.update_audio)
        self.update_button.pack()

        self.root.mainloop()

    def update_audio(self):
        gain = self.gain_value.get()
        processed_audio = self.process_audio(gain)
        print(f"Processed audio with gain {gain} dB")

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

if __name__ == "__main__":
    tuner = AudioTuner()
    try:
        tuner.start()
    except KeyboardInterrupt:
        tuner.stop()