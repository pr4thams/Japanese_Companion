import pyaudio
import wave
import keyboard

class Recorder:
    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def record_audio(self, output_filename, key='space'):
        # Create a PyAudio instance
        p = pyaudio.PyAudio()

        # Open a recording stream
        stream = p.open(format=pyaudio.paInt16, 
                        channels=self.channels, 
                        rate=self.rate, 
                        input=True, 
                        frames_per_buffer=self.frames_per_buffer)

        frames = []

        # Start recording when key is pressed
        print(f"Press and hold the '{key}' key to start recording...")
        keyboard.wait(key)  # wait for the key press

        print("Recording...")
        while keyboard.is_pressed(key):  # while the key is pressed
            data = stream.read(self.frames_per_buffer)
            frames.append(data)

        print("Recording stopped.")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()

        # Terminate the PortAudio interface
        p.terminate()

        # Check if any data was recorded
        if len(frames) > 0:
            # Save the recorded data to a WAV file
            wf = wave.open(output_filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            print("Recording saved.")
        else:
            print("No data recorded.")


if __name__ == "__main__":
    rec = Recorder()
    rec.record_audio('output.wav', key='space')
